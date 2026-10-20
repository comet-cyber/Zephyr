#requires -RunAsAdministrator
<#
Host diagnostic tool, not a board firmware API.
Capture only traffic matching the Titan MAC for a bounded time. Refuse to
replace an existing PktMon session or packet filter. Always stop the session
owned by this script and remove its temporary filter before exiting.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,

    [ValidateRange(15, 600)]
    [int]$DurationSeconds = 90
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$captureDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
[System.IO.Directory]::CreateDirectory($captureDirectory) | Out-Null
$captureLog = Join-Path $captureDirectory 'capture.log'
$captureStatus = Join-Path $captureDirectory 'status.txt'
$captureEtl = Join-Path $captureDirectory 'packets.etl'
$capturePcap = Join-Path $captureDirectory 'packets.pcapng'
$captureText = Join-Path $captureDirectory 'packets.txt'
$captureFilterName = 'ZephyrTitanUdp'
$captureStarted = $false
$captureFilterAdded = $false
$captureFailed = $false
$captureExe = Join-Path $env:SystemRoot 'System32\pktmon.exe'

function Write-CaptureLog {
    <# Internal helper: append a timestamped progress message to the log. #>
    param([string]$Message)
    $captureMessage = '{0} {1}' -f (Get-Date -Format 'HH:mm:ss.fff'), $Message
    $captureMessage | Out-File -LiteralPath $captureLog -Append -Encoding UTF8
}

function Invoke-CaptureCommand {
    <# Internal helper: run PktMon, preserve its output, and fail on errors. #>
    param([string[]]$Arguments)
    $captureCommandOutput = & $captureExe @Arguments 2>&1
    $captureCommandExit = $LASTEXITCODE
    $captureCommandOutput | Out-File -LiteralPath $captureLog -Append -Encoding UTF8
    if ($captureCommandExit -ne 0) {
        throw "PktMon failed ($captureCommandExit): $($Arguments -join ' ')"
    }
}

'STARTING' | Set-Content -LiteralPath $captureStatus -Encoding ASCII
try {
    # A pre-existing trace belongs to somebody else: never stop it.
    $ErrorActionPreference = 'Continue'
    $captureExistingSession = & logman.exe query PktMon -ets 2>&1
    $captureSessionQueryExit = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'
    if ($captureSessionQueryExit -eq 0) {
        throw 'An existing PktMon trace is active; leaving it untouched.'
    }

    $captureExistingFilters = & $captureExe filter list 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not query existing PktMon filters.'
    }
    $captureExistingFilters | Out-File -LiteralPath $captureLog -Append -Encoding UTF8
    if (($captureExistingFilters -join "`n") -match '(?m)^\s*\d+\s+') {
        throw 'Existing PktMon filters found; leaving them untouched.'
    }

    Invoke-CaptureCommand -Arguments @('filter', 'add', $captureFilterName,
                                       '-m', '74-90-50-01-02-03')
    $captureFilterAdded = $true
    Invoke-CaptureCommand -Arguments @('start', '--capture', '--comp', 'all',
        '--pkt-size', '0', '--flags', '0x03F', '--file-size', '128',
        '--log-mode', 'multi-file', '--file-name', $captureEtl)
    $captureStarted = $true
    Invoke-CaptureCommand -Arguments @('list')
    Write-CaptureLog "READY: capturing Titan traffic for $DurationSeconds seconds."
    'READY' | Set-Content -LiteralPath $captureStatus -Encoding ASCII

    $captureDeadline = (Get-Date).AddSeconds($DurationSeconds)
    $captureCounterTime = [datetime]::MinValue
    while ((Get-Date) -lt $captureDeadline) {
        if (Test-Path -LiteralPath (Join-Path $captureDirectory 'stop.request')) {
            break
        }
        if (((Get-Date) - $captureCounterTime).TotalSeconds -ge 5) {
            & $captureExe counters 2>&1 |
                Out-File -LiteralPath (Join-Path $captureDirectory 'counters.txt') -Encoding UTF8
            $captureCounterTime = Get-Date
        }
        Start-Sleep -Seconds 1
    }
}
catch {
    $captureFailed = $true
    Write-CaptureLog "ERROR: $($_.Exception.Message)"
}
finally {
    if ($captureStarted) {
        try {
            Invoke-CaptureCommand -Arguments @('stop')
            # Multi-file mode adds a number even when only one ETL is produced.
            $captureFiles = @(Get-ChildItem -LiteralPath $captureDirectory -Filter 'packets*.etl')
            if ($captureFiles.Count -eq 0) {
                throw 'PktMon stopped without producing an ETL file.'
            }
            foreach ($captureFile in $captureFiles) {
                $captureExportBase = if ($captureFiles.Count -eq 1) { 'packets' } else { $captureFile.BaseName }
                $capturePcap = Join-Path $captureDirectory ($captureExportBase + '.pcapng')
                $captureText = Join-Path $captureDirectory ($captureExportBase + '.txt')
                Invoke-CaptureCommand -Arguments @('etl2pcap', $captureFile.FullName, '--out', $capturePcap)
                Invoke-CaptureCommand -Arguments @('etl2txt', $captureFile.FullName, '--out', $captureText, '--hex')
                if ((Get-Item -LiteralPath $capturePcap).Length -le 192) {
                    Write-CaptureLog 'WARNING: export contains no packet data; counters alone do not validate capture.'
                }
            }
        }
        catch {
            $captureFailed = $true
            Write-CaptureLog "STOP/EXPORT ERROR: $($_.Exception.Message)"
        }
    }
    if ($captureFilterAdded) {
        # This Windows version removes all filters at once. Clear only when
        # the current table contains our single filter and no foreign row.
        $captureFinalFilters = & $captureExe filter list 2>&1
        $captureFinalRows = @($captureFinalFilters | Where-Object { $_ -match '^\s*\d+\s+' })
        if ($LASTEXITCODE -eq 0 -and $captureFinalRows.Count -eq 1 -and
            ($captureFinalRows[0] -like "*$captureFilterName*")) {
            try {
                Invoke-CaptureCommand -Arguments @('filter', 'remove')
            }
            catch {
                $captureFailed = $true
                Write-CaptureLog "FILTER CLEANUP ERROR: $($_.Exception.Message)"
            }
        }
        else {
            $captureFailed = $true
            Write-CaptureLog 'Filter table changed; manual cleanup of ZephyrTitanUdp may be required.'
        }
    }
    $captureFinalStatus = if ($captureFailed) { 'ERROR' } else { 'DONE' }
    $captureFinalStatus | Set-Content -LiteralPath $captureStatus -Encoding ASCII
    Write-CaptureLog $captureFinalStatus
}

if ($captureFailed) { exit 1 }
