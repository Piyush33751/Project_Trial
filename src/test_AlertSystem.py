from hal import hal_input_switch as input_switch
import test_TempSmoke as tempsmoke

def alert():
    input_switch.init()
    smoke = tempsmoke.get_ir_sensor_state()
    temp = tempsmoke.get_temp_state()
    switchstate = input_switch.read_slide_switch()

    print(f"IR: {smoke}, Temp: {temp}, Switch: {switchstate}")  # Debug output

    if (smoke == True and temp == True) or switchstate == 1:
        return True
    else:
        return False