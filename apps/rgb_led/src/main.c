/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * Titan Mini 板载 RGB LED 演示。
 *
 * 灯是共阳 GPIO，不是 PWM：
 *   红 P109 / led2，绿 P108 / led1，蓝 P110 / led3，低电平点亮。
 * 板 DTS 已经写成 gpio-leds + GPIO_ACTIVE_LOW，所以
 * gpio_pin_set_dt(..., 1) 表示逻辑点亮，不必自己反相。
 *
 * 控制台和 shell 都走板默认 UART2（SCI2，P801/P802，115200）。
 */

#include <errno.h>
#include <stddef.h>
#include <stdint.h>

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/drivers/gpio.h>

/* 应用侧别名在 app.overlay 里接到板级 led1/led2/led3。 */
static const struct gpio_dt_spec red_led = GPIO_DT_SPEC_GET(DT_ALIAS(red_led), gpios);
static const struct gpio_dt_spec green_led = GPIO_DT_SPEC_GET(DT_ALIAS(green_led), gpios);
static const struct gpio_dt_spec blue_led = GPIO_DT_SPEC_GET(DT_ALIAS(blue_led), gpios);

struct rgb_color {
	const char *name;
	uint8_t r;
	uint8_t g;
	uint8_t b;
};

/* 1 = 亮，0 = 灭。顺序与官方 RT-Thread RGB 例程一致。 */
static const struct rgb_color palette[] = {
	{ "off",    0, 0, 0 },
	{ "red",    1, 0, 0 },
	{ "green",  0, 1, 0 },
	{ "blue",   0, 0, 1 },
	{ "yellow", 1, 1, 0 },
	{ "cyan",   0, 1, 1 },
	{ "magenta",1, 0, 1 },
	{ "white",  1, 1, 1 },
};

/**
 * @brief 把一颗 gpio-leds 子节点配成输出。
 *
 * gpio_is_ready_dt / gpio_pin_configure_dt 是应用可直接调用的 Zephyr GPIO API，
 * 不是 RA 寄存器驱动入口。
 */
static int led_setup(const struct gpio_dt_spec *led, const char *name)
{
	int ret;

	if (!gpio_is_ready_dt(led)) {
		printk("Error: %s GPIO is not ready\n", name);
		return -ENODEV;
	}

	ret = gpio_pin_configure_dt(led, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		printk("Error: failed to configure %s (%d)\n", name, ret);
		return ret;
	}

	return 0;
}

/** @brief 按逻辑亮灭写三通道。gpio_pin_set_dt 是应用 API。 */
static int rgb_set(uint8_t r, uint8_t g, uint8_t b)
{
	int ret;

	ret = gpio_pin_set_dt(&red_led, r);
	if (ret < 0) {
		return ret;
	}
	ret = gpio_pin_set_dt(&green_led, g);
	if (ret < 0) {
		return ret;
	}
	return gpio_pin_set_dt(&blue_led, b);
}

int main(void)
{
	int ret;

	printk("Titan Mini RGB LED (GPIO, UART2). Shell prompt: uart:~$\n");
	printk("Type help, kernel stacks, or device list\n");

	if (led_setup(&red_led, "red") ||
	    led_setup(&green_led, "green") ||
	    led_setup(&blue_led, "blue")) {
		return 0;
	}

	while (1) {
		for (size_t i = 0; i < ARRAY_SIZE(palette); i++) {
			ret = rgb_set(palette[i].r, palette[i].g, palette[i].b);
			if (ret < 0) {
				printk("Error: RGB write failed (%d)\n", ret);
				return 0;
			}
			k_msleep(800);
		}
	}

	return 0;
}
