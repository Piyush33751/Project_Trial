from picamera2 import Picamera2, Preview
import time
def photo():
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920,1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    #picam2.start_preview(Preview.QTGL)
    picam2.start()
    time.sleep(2)
    picam2.capture_file("/home/pi/ET0735/Smart_FireAlert_System_AIoT/src/static/test.jpg")
    picam2.stop()
    