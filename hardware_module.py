
##########Import##########
import argparse
import io
import picamera
import time
import RPi.GPIO as gpio
import requests

from google.cloud import vision
from google.cloud.vision import types

##########Google Vision & Carnumber Detect Function########## 
def Carnumber_Detect(image_file):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.text_detection(image=image)
    labels = response.text_annotations
    carnum=""
    sliced_carnum=""
    for label in labels:
        #print(label.description)
        if len(label.description) >= 8 and len(label.description) <= 13:
            carnum=label.description
    # carnumber detection performence up
    for i in range(0, len(carnum)):
        if carnum[i:i+1].isdigit():
            carnum = carnum[i:]
            break
    for i in reversed(range(len(carnum))):
        if carnum[i].isdigit():
            carnum = carnum[0:i+1]
            break
    carnum=carnum.replace(" ", "")
    #if(carnum[0:1].isdigit()):
        #Sent Carnumber Information to Server
    result = requests.post('http://35.200.117.1:8080/control.jsp?type=reservation&action=select&from=raspberry&carNumber='+carnum)
    if carnum==result.text[14:21]:
        print(carnum)
        return True
    else:
        return False

###########PiCamera Capture Function##########
def Camera_Capture():
	cam.start_preview()
	time.sleep(3)
	cam.stop_preview()
	cam.capture('/home/pi/Drive_Thru_ATM/picture/1.jpg')

##########Supersonic Sensor Detect Function##########
def Car_Detect():
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

	        while gpio.input(echo) == 0 :
	            pulse_start = time.time()

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
                if distance_detect[0] < 20 and distance_detect[1] < 20 and distance_detect[2] < 20 and distance_detect[0] != 0 and distance_detect[1] != 0:
	            print "Car Detected!"
	            break
	except :
	    gpio.cleanup()

##########Waiting Function##########
def Waiting():
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

	        while gpio.input(echo) == 0 :
	            pulse_start = time.time()

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
                if distance_detect[0] > 50 and distance_detect[1] > 50 and distance_detect[2] > 50 and distance_detect[0] != 0 and distance_detect[1] != 0:
	            print "Finish!"
	            break
	except :
	    gpio.cleanup()

##########Function Execution##########
cam=picamera.PiCamera()
while True:
	#1 Car Detect By Supersonic Sensor
	Car_Detect()
	#2 Capture the Carnumber By PiCamera
	Camera_Capture()
	#3 Carnumber Detect From Captured Carnumber
        for i in range(0,3):
            if __name__ == '__main__':
                if Carnumber_Detect('/home/pi/Drive_Thru_ATM/picture/1.jpg'):
                    break
	#4 Wait For Getting out from Carnumber Detecting System.
	Waiting()

