def buzzer():
    while (Humidity==1) and (Infared==1):
        buzzer.beep(0.5, 0.5,)
        led.set_output(1, 1)
        time.sleep(2)
        led.set_output(1, 0)
        time.sleep(2)
    lcd.lcd_clear()
    lcd.lcd_display_string("There is a fire detected", 1)
    lcd.lcd_display_string("Please evacuate", 2)
    alert=1




#if infa ==1
def servo/DCMotor():
    servo.set_servo_position(120)
    while alert==1:
        servo.set_servo_position(160)
        time.sleep(4)
        dc_motor.set_motor_speed(50)
    lcd.lcd_display_string("key pressed "  +str(keyvalue), 1)     
    lcd.lcd_display_string("servo/DC test ", 2)  
    servo.set_servo_position(20)
    time.sleep(1)  
    servo.set_servo_position(80)
    time.sleep(1)     
     servo.set_servo_position(120)
    time.sleep(1)            
     dc_motor.set_motor_speed(50)
     time.sleep(4)   
     dc_motor.set_motor_speed(0)
     time.sleep(2)