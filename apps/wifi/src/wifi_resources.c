#include <stddef.h>
#include <stdint.h>

#include <wiced_resource.h>

#include "wifi_firmware_flash.h"
#include "wifi_resources.h"

#ifndef WIFI_FW_IMAGE_SIZE
#error "WIFI_FW_IMAGE_SIZE must be supplied by the application CMakeLists.txt"
#endif

/*
 * 固件句柄只记录外部资源的位置和长度；固件字节本身不定义在这个镜像中。
 * WHD 后续会以该句柄为入口调用 platform_read_external_resource()。
 */
const resource_hnd_t wifi_firmware_image = {
	.location = RESOURCE_IN_EXTERNAL_STORAGE,
	.size = WIFI_FW_IMAGE_SIZE,
	.val.external_storage_context = NULL,
};

/* CLM 仍作为应用只读数据保留在 CM85 镜像中。 */
const unsigned char wifi_firmware_clm_blob_data[] = {
#include <wifi_clm_blob.inc>
};

const resource_hnd_t wifi_firmware_clm_blob = {
	.location = RESOURCE_IN_MEMORY,
	.size = sizeof(wifi_firmware_clm_blob_data),
	.val.mem = {
		.data = (const char *)wifi_firmware_clm_blob_data,
	},
};

/**
 * 从外部 OSPI Flash 的 whd-firmware 分区读取 Wi-Fi 固件。
 *
 * 该函数是 WHD 的资源接口回调，offset 和 maxsize 都是相对于固件起点
 * 的值。底层 wifi_firmware_flash_read() 再把相对偏移转换为分区内偏移。
 */
resource_result_t platform_read_external_resource(
	const resource_hnd_t *resource,
	uint32_t offset,
	uint32_t maxsize,
	uint32_t *size,
	void *buffer)
{
	uint32_t actual_size;

	if (resource == NULL || size == NULL ||
	    (buffer == NULL && maxsize != 0U)) {
		return RESOURCE_FILE_READ_FAIL;
	}

	if (offset > resource->size) {
		return RESOURCE_OFFSET_TOO_BIG;
	}

	actual_size = maxsize;
	if (actual_size > resource->size - offset) {
		actual_size = resource->size - offset;
	}

	if (wifi_firmware_flash_read(offset, buffer, actual_size) != 0) {
		return RESOURCE_FILE_READ_FAIL;
	}

	*size = actual_size;
	return RESOURCE_SUCCESS;
}
