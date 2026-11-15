#ifndef WIFI_RESOURCES_H
#define WIFI_RESOURCES_H

#include <stdint.h>

#include <wiced_resource.h>

/**
 * 由 WHD resource_read() 调用的应用侧外部资源读取回调。
 *
 * @param resource  外部资源句柄。
 * @param offset    相对于资源起点的读取偏移。
 * @param maxsize   调用方缓冲区最多可接收的字节数。
 * @param size      返回实际读取的字节数。
 * @param buffer    调用方提供的目标缓冲区。
 * @return          WHD 资源读取结果码。
 */
resource_result_t platform_read_external_resource(
	const resource_hnd_t *resource,
	uint32_t offset,
	uint32_t maxsize,
	uint32_t *size,
	void *buffer);

#endif
