#ifndef WIFI_FIRMWARE_FLASH_H
#define WIFI_FIRMWARE_FLASH_H

#include <stddef.h>
#include <stdint.h>

/*
 * 从外部 Flash 的 Wi-Fi 固件分区读取数据。
 * image_offset 是相对固件起点的偏移，不是 CPU 映射地址。
 */
int wifi_firmware_flash_read(uint32_t image_offset, void *buffer, size_t length);

#endif
