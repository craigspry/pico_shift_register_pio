cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)
project(test_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(shift_register
shift_register.c
)
pico_generate_pio_header(shift_register ${CMAKE_CURRENT_LIST_DIR}/shift_reg.pio)

pico_enable_stdio_usb(shift_register 1)
pico_enable_stdio_uart(shift_register 1)
pico_add_extra_outputs(shift_register)
target_link_libraries(shift_register pico_stdlib hardware_pio)