# SAFETY

更新日期：2026-10-24

## 下载边界

- 项目启动不代表授权下载；当前未授权任何目标板固件写入。
- Mini 默认保护原始 Stage 0；工作区旧文档对当前板上固件有不同历史判断，必须读回确认，不能据其猜测覆盖。
- Titan 的当前固件未知，同样需先备份 Code MRAM、审计目标镜像，再取得当前消息的明确下载同意。
- 不写 Config Area/OFS、OTP、分区、DLM、密钥或生命周期区域；不启动 Device Partition Manager SCI，不升级 J-Link 固件。
- Code MRAM 物理窗口为 0x02000000 至 0x02100000（末地址不含），具体 CM85 分配依最终 DTS/链接结果；审计排除 0x02C9/0x02E1 及其它配置记录。
- ELF 以实际文件加载内容的物理地址/LMA 审计，区分 SRAM VMA 与 MRAM LMA；HEX 检查所有地址记录，不能只改变 OFS 值就视为安全。
- 配置区可能撑大原始 bin；未审计禁止直接 west flash。

## 参考与恢复

工作区安全材料：F:\zephyr\.agents\SAFETY.md。主链路候选为已验证的 IAR J-Link 8.74、S/N 601012527、SWD 1000 kHz、R7KA8P1KF_CPU0；在 Zephyr runner 中使用前核对实际 DLL/程序路径，不自动换探针版本。

Mini 已知 Stage 0 对照：0x02000000–0x020011FF；SHA-256 为 3F13821669C519682EE74BFAFEEA6676EC079C6FBCC5797537D9927FD4E2CDE4。此值仅用于原始 Stage 0 恢复对照，不代表当前实物读回值，更不能用于 Titan。

## Linux 网络与密钥

不覆盖既有 SSH 所用物理网卡配置；新增实验配置先记录现状。跨网络通信已纳入项目目标，公网入口及 VPS 方案尚未选择；如后续涉及现有 AWS 服务或网络变更，按用户 AWS 操作规则说明影响并确认。私钥不写 .agents/Git/对话，示例密钥不作真实实验长期密钥。
