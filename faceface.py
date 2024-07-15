import cv2
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import sys 
import requests
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch
from PIL import Image,ImageDraw,ImageFont
import json

# Raspberry Pi pin information
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
directory = os.getcwd()

doInterrupt =0
showOn = 0
data = ''
logging.basicConfig(level=logging.DEBUG)
    
def show(data):
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    Moisture_channel = AnalogIn(ads, ADS.P2)
    LDR_channel = AnalogIn(ads, ADS.P3)
    LM35_channel = AnalogIn(ads, ADS.P1)
    ID = "29f1345812705a07abc5174a67481dd4de1f1f9c7231c3b92c22d2eab4fb4476"
    ADC_16BIT_MAX = 65536
    lm35_constant = 10.0/1000
    ads_InputRange = 4.096
    #For Gain = 1; Otherwise change accordingly
    ads_bit_Voltage = (ads_InputRange * 2) / (ADC_16BIT_MAX - 1)

    #Initial variables
    Moisture_Recent = 100
    HighIn_DataSent = 0
    LowIn_DataSent = 0
    Thirsty_DataSent = 0
    Savory_DataSent = 0
    Happy_DataSent = 0
    TemperatureDataSent = 0

    def _map(x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


GPIO.setmode(GPIO.BCM)

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = video_capture.read()
    dataobj = {            "status": data,
    }

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Process the detected faces
    for (x, y, w, h) in faces:
        # Do something with the detected faces
        # For example, you can print the coordinates of each face
        print(f"Detected face: x={x}, y={y}, width={w}, height={h}")
        data = 'heart'

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    try:
        disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=90000000,rst=RST,dc=DC,bl=BL)
        disp.Init() # Initialize library.
        disp.clear() # Clear display.
        bg = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(bg)
        # display with hardware SPI:
        for i in range(90):
            if (doInterrupt==1):
                doInterrupt = 0
                break
            else:
        
                image = Image.open(directory+'/emotion/'+data+'/frame'+str(i)+'.png')
                image = image.rotate(180)
                disp.ShowImage(image)
        showOn = 0
        disp.module_exit()
        logging.info("quit:")
    except IOError as e:
        logging.info(e)    
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

def main():
    global doInterrupt, showOn, data
    previousData = 'happy'
    while True:
        if (previousData != data):
            print(data)
            doInterrupt = 1
            previousData = data
            show(data)

# Release the video capture
video_capture.release()
