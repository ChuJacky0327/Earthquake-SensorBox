import smbus
import time
import RPi.GPIO as GPIO
from time import sleep
import math
import serial
import random
from paho.mqtt import client as mqtt_client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json  
import busio
import board
import adafruit_adxl34x
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib#save model
from sklearn import tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
COM_PORT = '/dev/ttyACM0'
BAUD_RATES = 9600
ser = serial.Serial(COM_PORT ,BAUD_RATES)

broker = 'broker.hivemq.com'
port = 1883
topic = "CHU"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set("jacky","0327")
    client.connect(broker, port)
    return client


def publish(client,text):
    msg_count = 0     
    msg = f"messages: {msg_count}\n{text}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1
    #time.sleep(100)



# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

class ADXL345:

    address = None

    def __init__(self, address = 0x53):        
        self.address = address
        self.setBandwidthRate(BW_RATE_100HZ)
        self.setRange(RANGE_16G)
        self.enableMeasurement()

    def enableMeasurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        bus.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = bus.read_byte_data(self.address, DATA_FORMAT)

        value &= ~0x0F;
        value |= range_flag;  
        value |= 0x08;

        bus.write_byte_data(self.address, DATA_FORMAT, value)
    
    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce = False):
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}


    

adxl345 = ADXL345()     
original = adxl345.getAxes(True)
    

while True:
    if __name__ == "__main__":
        # if run directly we'll just create an instance of the class and output 
        # the current readings
        adxl345 = ADXL345()
        
        axes = adxl345.getAxes(True)
        if ((abs(axes['x'] - original['x']) >= 0.1) or (abs(axes['y'] - original['y']) >= 0.1) or (abs(axes['z'] - original['z']) >= 0.1) ):#0.1
            print ("   x = %.3fG" % ( axes['x'] - original['x']))
            print ("   y = %.3fG" % ( axes['y'] - original['y']))
            print( "   z = %.3fG" % ( axes['z'] - original['z']))
            ax = axes['x'] - original['x']
            ay = axes['y'] - original['y']
            az = axes['z'] - original['z']
            data = [ax,ay,az]
            print(data)
            lr = joblib.load('adxl.model')
            #Predict = lr.predict([np.array([-9.4928,0.196133,2.27513])])
            Predict = lr.predict([data])

            if (Predict > 2) :           
                ser.write(b'earthquake2\n')
                print('off2')
                client = connect_mqtt()
                text1 = 'earthquake_intensity : '+str(Predict) + '| turn off gas'
                publish(client, text1)
                if (Predict > 4) :           
                    ser.write(b'earthquake4\n')
                    print('off4')
                    client = connect_mqtt()
                    text2 = 'turn off air condition, light'
                    publish(client, text2)
                    if (Predict > 6) :           
                        ser.write(b'earthquake6\n')
                        print('off6')
                        client = connect_mqtt()
                        text3 = 'turn off refrigerator'
                        publish(client, text3)
                
            #time.sleep(1)
            original = adxl345.getAxes(True)        

        else: 
            print ("   x = %.3fG" % ( axes['x'] - original['x']))
            print ("   y = %.3fG" % ( axes['y'] - original['y']))
            print ("   z = %.3fG" % ( axes['z'] - original['z']))

        time.sleep(0.5) #Modify data acceptance time
ser.close()
