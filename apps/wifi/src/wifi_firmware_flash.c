
#include "wifi_firmware_flash.h"

#include <errno.h>

#include <zephyr/device.h>
#include <zephyr/drivers/flash.h>
#include <zephyr/storage/flash_map.h>

#ifndef WIFI_FW_IMAGE_SIZE
#error "WIFI_FW_IMAGE_SIZE must be supplied by the application CMakeLists.txt"
#endif

static const struct device *const firmware_flash =
    PARTITION_DEVICE(whd_firmware_partition);

/*
 * 读取 Wi-Fi 固件的一段数据。
 * 这是应用内部 API，之后 WHD 的外部资源读取钩子也会调用它。
 */
int wifi_firmware_flash_read(uint32_t image_offset, void *buffer, size_t length)
{
    if (buffer == NULL && length != 0U)
    {
        return -EINVAL;
    }

    if (image_offset > WIFI_FW_IMAGE_SIZE ||
        length > (size_t)(WIFI_FW_IMAGE_SIZE - image_offset))
    {
        return -EINVAL;
    }

    if (length == 0U)
    {
        return 0;
    }

    if (!device_is_ready(firmware_flash))
    {
        return -ENODEV;
    }

    return flash_read(firmware_flash,
                      PARTITION_OFFSET(whd_firmware_partition) + image_offset,
                      buffer,
                      length);
}
