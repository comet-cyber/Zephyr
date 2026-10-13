# CURRENT

> 更新日期：2026-10-06
>
> 每次会话先读本文件，做完当前增量再改下一阶段。不要一次铺开后面所有 Z。

## 现在停在哪

**Z0 未完成。** 工作区和 `apps/rgb_led` 能编，overlay 已关掉 `option_setting_*`，hex 人工看过没有 `0x02C9` / `0x02E1`。缺三件事：

1. 可重复的镜像守门脚本
2. 当前板上 Code MRAM 备份
3. 用户当次明确同意下载

板上跑的仍应是裸机系统监视器，不是 Zephyr。

## 下一会话：Z0-T1 守门脚本

目标：不碰板，先让“能不能下”变成一条命令。

**要做：**

- 新增 `F:\zephyr\scripts\audit_image.py`
- 输入：elf 或 hex
- 白名单：Code MRAM `0x02000000-0x02100000`
- 命中 OFS/OTP 或其它窗口 → 退出码非 0，打印越界段
- 用 `apps/rgb_led` 现有产物做 PASS 样例

**不要做：** `west flash`、改 Config Area、升级 J-Link、动 ECSDC、新开应用。

**你需要准备的：** 这一步不用接板。下一小步 Z0-T3 备份 MRAM 才要 J-Link。

## 之后怎么推进（一次只做一块）

| 顺序 | 增量 | 你能看见什么 |
| --- | --- | --- |
| Z0-T2 | 抽出共用 OFS overlay | 应用 overlay 变短，守门仍然 PASS |
| Z0-T3 | 备份 Code MRAM | `F:\zephyr\backups\` 里有当前固件，不含配置区 |
| Z1 | 第一次下载 rgb_led | RGB 循环 + UART2 有字。必须当次同意 |
| Z2 | 追 DT，overlay 换灯 | 不改 `main.c` 也能换颜色通道 |
| Z3 | SW1 接管灯 | 按键能改灯 |
| Z4 | 收口树外骨架 | 构建目录和文件职责固定 |
| Z5 | 灯/键拆线程 | 按键时灯循环不停 |
| Z6 | 自定义 shell 命令 | `rgb red` 这类命令改灯 |
| Z7 | LOG 替换 printk | 串口干净、能按级别过滤 |
| Z8 | I2C 对原理图 | 有 HWT101 需求再开 |

完整验收标准和暂缓项见 [`PLAN.md`](PLAN.md)。
