from hal import hal_temp_humidity_sensor as temp_humid_sensor
from hal import hal_ir_sensor as ir_sensor

def get_ir_sensor_state():
    infrared = False    #as long as ir value 
    #ir value returned is a boolean value, not a integer
    ir_value = ir_sensor.get_ir_sensor_state()
    if ir_value == True:
        infrared = True
    
    return infrared

def get_temp_state():
    temp = False
    temperature, humidity= temp_humid_sensor.read_temp_humidity()
    if temperature > 20000:
        temp = True
    else:
        temp = False

    return temp