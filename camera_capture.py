import picamera
import time
cam = picamera.PiCamera()
cam.start_preview()
time.sleep(10)
cam.stop_preview()
cam.capture('/home/pi/Drive_Thru_ATM/picture/1.jpg')
