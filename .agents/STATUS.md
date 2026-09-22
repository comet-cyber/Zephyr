# STATUS

> 更新日期：2026-09-22

## 项目

在 `F:\zephyr` 用 Zephyr 学习 Titan Mini（`ra8p1_titan_mini`），默认 Cortex-M85 / CPU0。

## 当前阶段

**Z0：工作区与下载安全基线。** `.agents` 已初始化。工具链和板支持存在，但默认构建产物 **不能下载**。

状态：`in_progress`（工作区可用） / 板上 Zephyr：`not verified`

## 已核对的工作区事实

- west topdir：`F:\zephyr`
- manifest：`F:\zephyr\zephyr\west.yml`，west 1.5.0，Python 3.12.14（`F:\zephyr\.venv`）
- Zephyr 版本字符串：`4.4.99`（主线，指向 4.5 工作草稿）
- 当前 `zephyr` 提交：`4c6971ba90a`（`v4.4.0-14199-g4c6971ba90a`）
- SDK：`F:\zephyr\.sdk`，`sdk_version` 文件为 `1.0.1`
- 包装 Git：`comet-cyber/Zephyr`，`main` 与 `origin/main` 同步；只跟踪工作区配置，不跟踪上游源码
- west 能列出板：`ra8p1_titan_mini`，qualifiers `r7ka8p1kflcac/cm85` 与 `r7ka8p1kflcac/cm33`
- Renesas HAL：`modules/hal/renesas` @ `f2eb9bc7352f4dadae08e9f5f16b05bb26779b87`

## 已存在但未验收的构建

2026-09-04 曾构建：

```text
west build -p always -b ra8p1_titan_mini/r7ka8p1kflcac/cm85 samples\basic\blinky
```

产物在 `F:\zephyr\zephyr\build\`：

- `zephyr.elf` 入口 `0x02000C45`，Code MRAM 主段约 `0x02000000-0x02007390`
- `zephyr.hex` **含 Config Area / OFS / OTP 记录**，例如：
  - `0x02C9F040`、`0x02C9F044`、`0x02C9F074`
  - `0x02C9F0C0`（OFS1_SEC）数据字节 `FF FF FF FD`
  - `0x02C9F200`、`0x02E17700`（OTP PBPS 段）
- `zephyr.bin` 约 14.1 MB，是被 option-setting 高地址撑开的 padded 镜像，禁止当下载文件使用

结论：这次 blinky **只证明 CMake/ninja 能编过，不证明可安全下载，更不证明板上跑过。** 在下载守门脚本通过之前，禁止 `west flash`。

## 与裸机工程的关系

Titan Mini 裸机系统监视器仍在：

`F:\embedded_systems_learning\projects\titan-mini-system-monitor`

该项目 Stage 2（e² studio + FSP + HWT101 I²C）已完成。板上当前运行的应是那套固件，不是 Zephyr。第一次下 Zephyr 会覆盖 Code MRAM。

裸机侧已验证的调试器基线仍适用：

- J-Link S/N `601012527`
- 设备名 `R7KA8P1KF_CPU0`
- SWD 1000 kHz
- 不升级探针固件，不替换已验证的 IAR J-Link DLL `8.74`（Zephyr 侧若改用系统 J-Link，下载前要单独确认）

## 阻塞

1. 没有 Code MRAM 纯净镜像审计工具（必须拒绝 Config Area / OFS / OTP 地址）。
2. 默认 RA8P1 linker 在独立应用（非 MCUboot 应用镜像）时会链入 `option_setting_*` 段。
3. 用户尚未在本 Zephyr 轨明确批准第一次下载。
4. 尚未备份当前板上 Code MRAM。

## 下一步

1. 做下载守门：解析 `zephyr.hex` / ELF PHDR，只允许 Code MRAM `0x02000000-0x02100000`。
2. 用 overlay 关掉 `option_setting_*` 节点，重编 `hello_world` 或 `blinky`，直到 hex 不含 `0x02C9xxxx` / `0x02E1xxxx`。
3. 备份当前 Code MRAM 后，再请求用户批准第一次 `west flash`。
4. 用 UART2 或 LED1 做板上验收。

## 未做

- 板上运行 Zephyr
- 双核 CM33
- MCUboot
- 以太网 / SD / USB
- 树外正式应用仓库结构（`apps/` 尚未创建）
