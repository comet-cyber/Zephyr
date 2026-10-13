# Zephyr 学习工作区

更新日期：2026-10-06

本目录是 `F:\zephyr` 的项目级持久上下文。开始工作先读本文件，再用代码、west、构建产物和板上证据核对；冲突以实际证据为准。

## 这是什么

- 工作区：`F:\zephyr`（west topdir）
- 目标板：Ruiside / RT-Thread **Titan Mini**，Zephyr 板名 `ra8p1_titan_mini`
- 默认核：Cortex-M85 / CPU0，完整 board target 为  
  `ra8p1_titan_mini/r7ka8p1kflcac/cm85`
- 学习状态：刚入门。工作区和 `apps/rgb_led` 能编，OFS overlay 已有，但 **还没有守门脚本，也没有经过批准的板上 Zephyr 映像**。
- 学习载体：`F:\zephyr\apps\rgb_led`。阶段任务见 [`PLAN.md`](PLAN.md)，当前增量见 [`CURRENT.md`](CURRENT.md)。

这是独立的 Zephyr 学习轨，不是 `F:\embedded_systems_learning` 里 Titan Mini 系统监视器项目的延续。两套工程共用同一块物理板，但固件会互相覆盖。

## 每次会话怎么开始

1. 读 [`CURRENT.md`](CURRENT.md) 看这一次只做什么。
2. 读 [`STATUS.md`](STATUS.md) 看阶段和阻塞项。
3. 读 [`SAFETY.md`](SAFETY.md)。涉及下载、复位、配置区、分区或 OTP 时必须遵守。
4. 按 [`PLAN.md`](PLAN.md) 推进当前增量，不要一次铺开全部外设。
5. 板级引脚和 board target 查 [`BOARD.md`](BOARD.md)。
6. 命令和环境查 [`TOOLCHAIN.md`](TOOLCHAIN.md)。
7. 有意义的结论、验证或阻塞写回 `STATUS.md`；决策写入 [`DECISIONS.md`](DECISIONS.md)。

## 文件

| 文件 | 用途 |
| --- | --- |
| [`CURRENT.md`](CURRENT.md) | 当前增量，一次只做这一块 |
| [`STATUS.md`](STATUS.md) | 当前状态、已验证事实、下一步 |
| [`PLAN.md`](PLAN.md) | Z0–Z8 阶段与验收标准 |
| [`SAFETY.md`](SAFETY.md) | 下载与配置区红线 |
| [`BOARD.md`](BOARD.md) | Titan Mini 在 Zephyr 中的板级事实 |
| [`TOOLCHAIN.md`](TOOLCHAIN.md) | west / SDK / J-Link 命令 |
| [`DECISIONS.md`](DECISIONS.md) | 已做决策，避免重复讨论 |

无证据不得把状态标成 `verified`。不要把密钥、完整原始日志或大段 west 输出贴进 `.agents`。

## 仓库边界

- 包装仓库：`git@github.com:comet-cyber/Zephyr.git`，当前分支 `main`。
- 被 gitignore 的内容：`.venv/`、`.sdk/`（旧路径）、`toolchains/`、`.west/`、`zephyr/`、`modules/`、`bootloader/`、`tools/`、`build/`。
- `.agents/` 应纳入 Git。上游 Zephyr 源码由 west 管理，不提交进包装仓库。
- 应用代码以后放 `F:\zephyr\apps\<name>\`，不要在 `zephyr/samples/` 里改上游示例当长期工程。
