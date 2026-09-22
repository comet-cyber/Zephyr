# TOOLCHAIN

> 更新日期：2026-09-22

## 环境

在 PowerShell 中：

```powershell
Set-Location F:\zephyr
& F:\zephyr\.venv\Scripts\Activate.ps1
$env:ZEPHYR_SDK_INSTALL_DIR = 'F:\zephyr\.sdk'
$env:ZEPHYR_BASE = 'F:\zephyr\zephyr'
```

| 组件 | 路径 / 版本 |
| --- | --- |
| Python | `F:\zephyr\.venv`，3.12.14 |
| west | 1.5.0，`F:\zephyr\.venv\Scripts\west.exe` |
| SDK | `F:\zephyr\.sdk`，sdk_version `1.0.1` |
| 交叉编译器 | `F:\zephyr\.sdk\gnu\arm-zephyr-eabi\bin\arm-zephyr-eabi-gcc.exe` |
| CMake/Ninja | 使用 SDK/hosttools 与当前 PATH；不要改去用 STM32CubeCLT 的 CMake 除非构建失败时再查 |
| 包装 Git | `F:\zephyr` → `comet-cyber/Zephyr` |
| 上游 Zephyr git | `F:\zephyr\zephyr`，当前 `4c6971ba90a` |

VS Code 工作区已推荐 `ms-vscode.cpptools` 与 `kylemicallefbonnici.dts-lsp`，并设置了 Zephyr IDE Terminal。`zephyr-ide.json` 里 `projects` 仍为空。

## 常用命令

在 `F:\zephyr` 下执行。sample 路径相对于 `zephyr/` 或写绝对路径都可以。

列出板：

```powershell
west boards -n ra8p1_titan_mini
```

构建 hello_world（推荐作为安全下载的第一张映像）：

```powershell
west build -p always -b ra8p1_titan_mini/r7ka8p1kflcac/cm85 zephyr/samples/hello_world
```

构建 blinky：

```powershell
west build -p always -b ra8p1_titan_mini/r7ka8p1kflcac/cm85 zephyr/samples/basic/blinky
```

默认构建目录历史上是 `F:\zephyr\zephyr\build`。新的构建应显式放到工作区级目录，避免和上游树混在一起，例如：

```powershell
west build -p always -b ra8p1_titan_mini/r7ka8p1kflcac/cm85 -d F:\zephyr\build\hello_world zephyr/samples/hello_world
```

`F:\zephyr\build\` 已被 gitignore。

## 下载

**先读 [`SAFETY.md`](SAFETY.md)。** 当前默认产物不能 flash。

预期命令（守门 PASS 且用户同意之后）：

```powershell
west flash -d F:\zephyr\build\hello_world --runner jlink
```

板级 `board.cmake` 已传入：

```text
--device=R7KA8P1KF_CPU0
--reset-after-load
```

调试：

```powershell
west debug -d F:\zephyr\build\hello_world --runner jlink
```

备选 runner：`pyocd --target=R7KA8P1KF`。入门不用 pyocd。

## 审计时看哪些文件

以构建目录为例：

| 文件 | 看什么 |
| --- | --- |
| `zephyr/zephyr.stat` | section 地址，立刻能发现 `0x02c9` / `0x02e1` |
| `zephyr/zephyr.elf` | `readelf -l` / program headers |
| `zephyr/zephyr.hex` | 是否出现 `:0200000402C9`、`:0200000402E1` |
| `zephyr/zephyr.bin` | 体积若到数 MB，多半是 padded，不要下载 |
| `zephyr/zephyr.dts` | 最终 DT |
| `zephyr/.config` | 最终 Kconfig |
| `zephyr/runners.yaml` | flash runner 与 J-Link 参数 |

## 不要做的事

- 不要在 `zephyr/` 里长期改上游文件当自己的工程。板级 bug 可以记下来，修复走单独决策。
- 不要把 `west update` 当成日常命令；升级 Zephyr 是显式任务。
- 不要用系统 `C:\Python314` 或 `E:\env\yolo` 来跑本工作区 west。
- 不要把 STM32 OpenOCD 当成 RA8P1 的默认下载器。
