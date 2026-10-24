# OPEN

更新日期：2026-10-24

## 当前需要解决

- Titan CYW43438 的 Zephyr 适配：RA SDHC 补 CMD5/52/53、SDIO 数据传输及必要通知机制；板级 SDHI1、供电/唤醒 GPIO 和固件/模块参数核对。
- 两个网络的实际接入方式与公网入口：直接互为 peer，还是接受 VPS 中心转发。尚未检查任一侧是否有可达公网 IPv4/IPv6。
- 既有项目已 active，当前有线使用 eth0；不再要求重复项目启动。

## 可在对应增量前解决

- Titan 串口 COM18 的运行日志、RGB 点灯结果及当前固件恢复材料未记录；编译/下载成功由用户确认，不扩展为这些项已验证。

- 实际物理接口名称、MAC/IP、端口与网卡路由，先核对再分配，避免影响既有 SSH 网络。
- 鲁班猫实测 Debian 12，WireGuard 内核与工具已具备；抓包工具按实际实验需要核对。
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
