# OPEN

更新日期：2026-10-14

## 挡住启动

- Titan 大板实际使用 eth0 还是 eth1，以及 RJ45 接口和 DTS 节点的对应关系。
- 用户尚未明确说“项目启动”；这是 skill 的阶段门，不是下载授权。

## 可在对应增量前解决

- Titan 串口 COM18 的运行日志、RGB 点灯结果及当前固件恢复材料未记录；编译/下载成功由用户确认，不扩展为这些项已验证。

- 实际物理接口名称、MAC/IP、端口与网卡路由，先核对再分配，避免影响既有 SSH 网络。
- Ubuntu 版本、WireGuard 模块/工具与抓包工具是否存在。
- PSA Crypto/随机源初始化是否适配当前 RA8P1 构建；不承诺硬件加速。
- 跨重启时间戳递增方案：本地默认 uptime 不应直接当作可靠 RTC。
- 本地官方 sample CMakeLists 使用 ZEPHYR_WIREGUARD_MODULE_DIR，而协议实现已在 subsys 内；真正构建前核对该变量及依赖，不照抄。
- 采用 Titan 后，核对网口/控制台引脚和 PHY 对应关系。

## 已关闭

- 2026-10-14 Titan 编译/下载链路 → 用户明确确认已打通；VS Code 插件与 jlink runner 为实际开发入口，详情见 STATUS。
- 2026-10-14 探针身份 → 本机枚举为 SEGGER J-Link 类接口、UID 24060501、COM18，不按 DAPLink 假设配置。

- 本地有无 WireGuard：源码已读，存在原生 API、实现与示例；Kconfig 明确 EXPERIMENTAL。
- 项目目录：用户指定 F:\zephyr\apps\wireguard，不迁移到学习仓。
- 2026-10-13 首轮板卡 → Titan 大板；网络 → 网线直连、静态 IPv4；鲁班猫可 SSH；用户已有 Titan Mini 的 Zephyr 编译/烧录经验。
