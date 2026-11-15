#ifndef WIFI_NVRAM_IMAGE_DATA_H
#define WIFI_NVRAM_IMAGE_DATA_H

#include <stdint.h>

#include "wifi_resources.h"

/*
 * RESOURCE_READ_FROM_C_FILE 模式下，WHD 直接从这个数组取得 NVRAM。
 * wifi_nvram_blob.inc 由应用构建脚本把上游文本转换为 NUL 分隔的
 * key=value 条目，末尾双 NUL 并按 4 字节补齐。此模式下 WHD 不会
 * 转换文本换行；不能直接把 CRLF/LF 文本生成的字节数组交给芯片。
 */
static const unsigned char wifi_nvram_image[] = {
#include <wifi_nvram_blob.inc>
};

#endif
