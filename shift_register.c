#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "pico/binary_info.h"
#include "shift_reg.pio.h"
const uint LED_PIN = 25;

int main()
{

    const uint dataPIN = 13;
    const uint latchPIN = 14;
    const uint clockPIN = 15;

    bi_decl(bi_program_description("This is an implimentation of the 74HC595 shift register using PIO."));
    bi_decl(bi_1pin_with_name(LED_PIN, "On-board LED"));

    bi_decl(bi_1pin_with_name(dataPIN, "Data for shift register"));
    bi_decl(bi_1pin_with_name(latchPIN, "Latch for shift register"));
    bi_decl(bi_1pin_with_name(clockPIN, "Clock for shift register"));

    stdio_init_all();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    uint offset = pio_add_program(pio0, &shift_reg_program);
    uint sm = 0;
    shift_reg_program_init(pio0, sm, offset, clockPIN, latchPIN, dataPIN);
    __uint8_t i = 0;
    while (1)
    {
        gpio_put(LED_PIN, 0);
        sleep_ms(250);
        gpio_put(LED_PIN, 1);
        pio_sm_put_blocking(pio0, sm, i);
        i += 1;
        sleep_ms(250);
    }
}