import time
from threading import Thread
import queue

from hal import hal_led as led
from hal import hal_lcd as LCD
from hal import hal_adc as adc
from hal import hal_buzzer as buzzer
from hal import hal_moisture_sensor as moisture_sensor
from hal import hal_input_switch as input_switch
from hal import hal_ir_sensor as ir_sensor
from hal import hal_rfid_reader as rfid_reader
from hal import hal_servo as servo
from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_usonic as usonic
from hal import hal_dc_motor as dc_motor

import test_AlertSystem as AlertSys
import test_TempSmoke as tempsmoke

def main():
    #initialization of HAL modules
    led.init()
    adc.init()
    buzzer.init()
    moisture_sensor.init()
    input_switch.init()
    ir_sensor.init()
    servo.init()
    temp_humid_sensor.init()
    usonic.init()
    dc_motor.init()

    lcd = LCD.lcd()
    lcd.lcd_clear()

    
    while(True):
        alert = AlertSys.alert()

        if alert == False:
            lcd.lcd_clear()
            lcd.lcd_display_string("Have a nice day", 1)
            led.set_output(1, 0)
            dc_motor.set_motor_speed(0)
            servo.set_servo_position(75)
            time.sleep(3)

        else:
            buzzer.beep(0.1, 0.1, 16)
            for i in range(10):
                led.set_output(1, 1)
                time.sleep(0.5)
                led.set_output(1, 0)
                time.sleep(0.5)
            lcd.lcd_clear()
            lcd.lcd_display_string("Fire Detected!", 1)
            lcd.lcd_display_string("Please Evacuate", 2)
            servo.set_servo_position(160)
            time.sleep(2)
            dc_motor.set_motor_speed(50)
        
        
        time.sleep(0.5)  # Short delay to prevent CPU overuse

    


if __name__ == '__main__':
    main()