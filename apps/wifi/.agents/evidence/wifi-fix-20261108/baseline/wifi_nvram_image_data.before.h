#ifndef WIFI_NVRAM_IMAGE_DATA_H
#define WIFI_NVRAM_IMAGE_DATA_H

#include <stdint.h>

#include "wifi_resources.h"

/*
 * RESOURCE_READ_FROM_C_FILE 模式下，WHD 直接从这个数组取得 NVRAM。
 * wifi_nvram_blob.inc 由应用 CMake 从上游 NVRAM 文本生成，仍然属于
 * 主控镜像中的小型配置资源，不是外部 Flash 固件。
 */
static const unsigned char wifi_nvram_image[] = {
#include <wifi_nvram_blob.inc>
};

#endif
