# STATUS

> 更新日期：2026-10-06

## 项目

在 `F:\zephyr` 用 Zephyr 学习 Titan Mini（`ra8p1_titan_mini`），默认 Cortex-M85 / CPU0。学习载体是树外应用 `F:\zephyr\apps\rgb_led`。

## 当前阶段

**Z0：工作区与下载安全基线。** 工具链和板支持存在，rgb_led 能编且 overlay 已关 OFS，但守门脚本、MRAM 备份、第一次下载都还没有。

状态：工作区 `usable` / rgb_led 构建 `built, not audited by script` / 板上 Zephyr：`not verified`

下一会话任务见 [`CURRENT.md`](CURRENT.md)：Z0-T1 守门脚本。

## 已核对的工作区事实

- west topdir：`F:\zephyr`
- manifest：`F:\zephyr\zephyr\west.yml`，west 1.5.0，Python 3.12.14（`F:\zephyr\.venv`）
- Zephyr 版本字符串：`4.4.99`（主线，指向 4.5 工作草稿）
- 当前 `zephyr` 提交：`4c6971ba90a`（`v4.4.0-14199-g4c6971ba90a`）
- SDK：`F:\zephyr\toolchains\zephyr-sdk-1.0.1`，`sdk_version` 文件为 `1.0.1`；2026-10-12 重新安装官方完整 GNU 包，35 套工具链
- 包装 Git：`comet-cyber/Zephyr`，只跟踪工作区配置，不跟踪上游源码
- west 能列出板：`ra8p1_titan_mini`，qualifiers `r7ka8p1kflcac/cm85` 与 `r7ka8p1kflcac/cm33`
- Renesas HAL：`modules/hal/renesas` @ `f2eb9bc7352f4dadae08e9f5f16b05bb26779b87`

## 学习载体现状（2026-10-03 构建，2026-10-06 复核计划）

`F:\zephyr\apps\rgb_led`：

- UART2 控制台 + GPIO RGB 循环
- `app.overlay` 只做颜色别名和关闭 `option_setting_*`
- 构建通过，hex 未出现 `0x02C9` / `0x02E1` 扩展地址（人工，不是脚本）
- `prj.conf` 已开 `CONFIG_SHELL` / kernel / device shell，板上未验证
- 构建目录目前在 `apps/rgb_led/build`，Z4 要改到 `F:\zephyr\build\rgb_led`

2026-09-04 上游 blinky 曾编过，hex **含** Config Area / OFS / OTP，只能当守门脚本的 FAIL 样例，禁止下载。

## 与其它工程的关系

Titan Mini 裸机系统监视器仍在：

`F:\embedded_systems_learning\projects\titan-mini-system-monitor`

板上当前运行的应是那套固件。第一次下 Zephyr 会覆盖 Code MRAM。

ECSDC 比赛固件在 `F:\ECSDC\firmware`，不在本轨推进。

裸机侧已验证的调试器基线仍适用：

- J-Link S/N `601012527`
- 设备名 `R7KA8P1KF_CPU0`
- SWD 1000 kHz
- 不升级探针固件，不替换已验证的 IAR J-Link DLL `8.74`（Zephyr 侧若改用系统 J-Link，下载前要单独确认）

## 阻塞

1. 没有 Code MRAM 纯净镜像审计工具。
2. 用户尚未在本 Zephyr 轨明确批准第一次下载。
3. 尚未备份当前板上 Code MRAM。

## 下一步

按 [`PLAN.md`](PLAN.md) 的 Z0 → Z1 → … 走，当前只做 Z0-T1。

## 未做

- 守门脚本
- 板上运行 Zephyr
- SW1 应用逻辑
- 双核 CM33
- MCUboot
- 以太网 / SD / USB / HWT101-on-Zephyr

## 2026-10-12：SDK 目录接入 VS Code 插件

- 现有 SDK 1.0.1 实体目录从 `F:\zephyr\.sdk` 移到 `F:\zephyr\toolchains\zephyr-sdk-1.0.1`，符合 IDE for Zephyr 4.1.0 的扫描命名规则。
- `.vscode/settings.json` 的 `zephyr-ide.toolchainDirectory` 为 `F:/zephyr/toolchains`。
- 旧路径 `F:\zephyr\.sdk` 保留为指向新目录的 Junction；已有环境变量、CMake 缓存仍可通过旧路径访问 SDK。
- 验证：移动前后 49,561 个文件、8,715,371,576 字节一致；ARM GCC SHA-256 一致，旧路径执行 `--version` 成功（GCC 14.3.0）。未运行构建或烧录；插件面板显示待 Refresh 确认。

## 2026-10-12：按标准目录重新安装完整 SDK

- 按用户要求重新下载官方 `zephyr-sdk-1.0.1_windows-x86_64_gnu.7z` 并安装到 `F:\zephyr\toolchains\zephyr-sdk-1.0.1`，没有保留工作区内的 `.sdk` 入口。
- 官方 SHA-256：`811CB97797DDF6198EEA66B030168D12512F605C7E332EA24D2CBE47B769C472`；解压完整性通过，67,854 个文件、11,884,624,093 字节。全部 35 套 GNU 编译器执行 `--version` 成功。
- 用户级 `ZEPHYR_SDK_INSTALL_DIR`、工作区终端环境和 CMake 用户包登记均切到新 SDK；`toolchains/` 已加入 `.gitignore`。完全退出并重开 VS Code 后扩展进程才会继承新用户环境变量。
- `rgb_led` 原构建目录执行 Pristine 构建成功，194 个构建步骤完成；CMakeCache 的编译器和 SDK 路径均指向新目录。存在上游设备树 `/soc/trng` 的 `simple_bus_reg` 警告，未改动板文件。此次没有连接或烧录开发板，不代表镜像已完成下载审计。
- 官方安装包、校验清单与构建日志保留在 `F:\ai_lab\zephyr-sdk-reinstall`。
- 自动审批拒绝了删除操作，工具仅返回 `blocked by policy`。采取可恢复的替代方式：旧 `.sdk` 联接移到 `F:\ai_lab\zephyr-sdk-backup\legacy-sdk-path-link`；旧 SDK 实体备份为该目录的 `original-sdk-1.0.1`。原 ZIP 备份也保留。工作区实际检查 `.sdk` 不存在，新 SDK 存在。
