lcd = LCD.lcd()
lcd.lcd_clear()

if(temp_humid_sensor < 45):
    lcd.lcd_display_string("Have a Nice Day")
elif(temp_humid_sensor >= 45 and temp_humid_sensor < 100):
    lcd.lcd_display_string("There is fire, Exit here")
elif(temp_humid_sensor >= 100):
    lcd.lcd_display_string("There is fire, Evacuate to a safe location")


if(temp_humid_sensor >=100):
    led.set_output(1, 1)
    time.sleep(1)
    led.set_output(1, 0)
    time.sleep(1)
else:
     led.set_output(1, 0)