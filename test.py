##########Import##########
import argparse
import io
import picamera
import time
import RPi.GPIO as gpio
import requests;

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
    print(carnum)
    result = requests.post('http://35.200.117.1:8080/rasptest.jsp?carNumber='+carnum)
    print(result.text[14:21])

###########PiCamera Capture##########
cam = picamera.PiCamera()
cam.start_preview()
time.sleep(5)
cam.stop_preview()
cam.capture('/home/pi/Drive_Thru_ATM/picture/1.jpg')

##########Text Detection##########
if __name__ == '__main__':
    main('/home/pi/Drive_Thru_ATM/picture/1.jpg')

##########NFC Reader##########

