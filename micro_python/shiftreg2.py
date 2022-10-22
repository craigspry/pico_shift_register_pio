from machine import Pin
import utime
import random
import rp2

#define PINs according to cabling
dataPIN = 13
latchPIN = 14
clockPIN = 15

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

#set pins to output PIN objects
dataPIN=Pin(dataPIN)#, Pin.OUT)
latchPIN=Pin(latchPIN)#, Pin.OUT)
clockPIN=Pin(clockPIN)#, Pin.OUT)

@rp2.asm_pio(
    set_init=rp2.PIO.OUT_LOW,
    out_init=rp2.PIO.OUT_LOW,
    sideset_init=rp2.PIO.OUT_LOW,
    autopull=True
)
def shift_reg():
    """
    Send a byte (8 bits) to the DATA pin,
    one bit per cycle. Then create a pulse on
    the LATCH pin to display the 8 bits.
    """
    wrap_target()
    set(x, 7)                       # loop counter, loop 8 times
    label('bitloop')
    out(pins, 1)       .side(0)     # output the data and pulse the clock pin 
    jmp(x_dec, 'bitloop').side(1)          
    set(pins, 1)      # pulse the latch   
    set(pins, 0)
    wrap()
    
sm = rp2.StateMachine(0, shift_reg, 
                      sideset_base=clockPIN,    # CLOCK pin
                      set_base=latchPIN,        # LATCH pin
                      out_base=dataPIN,        # DATA pin
                      push_thresh=8,
                     )

i = 0
sm.active(1)
while True:
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    
    # shift_update_int(int(temperature),dataPIN,clockPIN,latchPIN)
    sm.put(int(temperature).to_bytes(1, 'big'))
    print(int(temperature))
    i += 1
    # bit_string = str(random.randint(0, 1))+bit_string[:-1]
    utime.sleep(2)