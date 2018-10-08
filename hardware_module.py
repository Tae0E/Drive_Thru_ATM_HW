##########Import##########
import argparse
import io
import picamera
import time
import RPi.GPIO as gpio

from google.cloud import vision
from google.cloud.vision import types

##########Google Vision Function########## 
def main(image_file):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    labels = response.text_annotations
    for label in labels:
        print(label.description)

##########Supersonic Sensor Detection##########
gpio.setmode(gpio.BCM)

trig = 13
echo = 19

print "Supersonic Sensor Start"

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
distance_detect = [0, 0, 0]
try :
    while True :
        gpio.output(trig, False)
        time.sleep(0.5)

        gpio.output(trig, True)
        time.sleep(0.00001)
        gpio.output(trig, False)

        while gpio.input(echo) == 0 :                                                       pulse_start = time.time()

        while gpio.input(echo) == 1 :
            pulse_end = time.time()
            
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        print "Distance : ", distance, "cm"
 
        if distance_detect[0] == 0:
            distance_detect[0] = distance
        else:
            if distance_detect[1] == 0:
                distance_detect[1] = distance
            else:
                if distance_detect[2] == 0:
                    distance_detect[2] = distance
                else:
                    del distance_detect[0]
                    distance_detect.append(distance)
        print '1 : ', distance_detect[0], ' 2 : ', distance_detect[1], ' 3 : ', distance_detect[2]
        if distance_detect[0] < 20 and distance_detect[1] < 20 and distance_detect[2] < 20 and distance_detect[0] != 0 and distance_detect[1] != 0 and distance_detect[2] != 0:
            print "Car Detected!"
            break
except :
    gpio.cleanup()

###########PiCamera Capture##########
cam = picamera.PiCamera()
cam.start_preview()
time.sleep(10)
cam.stop_preview()
cam.capture('/home/pi/Drive_Thru_ATM/picture/1.jpg')

##########Text Detection##########
if __name__ == '__main__':
    main('/home/pi/Drive_Thru_ATM/picture/1.jpg')

##########NFC Reader##########

