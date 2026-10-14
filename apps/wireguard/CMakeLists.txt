cmake_minimum_required(VERSION 3.28.0)

# 加载 Zephyr 构建系统，并创建应用目标 app。
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(wireguard)

# 将应用入口源文件加入 app；驱动和协议栈由 Kconfig 选择。
target_sources(app PRIVATE src/main.c)
