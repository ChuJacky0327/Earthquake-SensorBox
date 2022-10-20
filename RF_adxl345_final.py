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
import smbus
import time
import RPi.GPIO as GPIO
from time import sleep
import math
import serial
import random
from paho.mqtt import client as mqtt_client

i2c = busio.I2C(board.SCL, board.SDA)
#i2c=board.I2C()
acc = adafruit_adxl34x.ADXL345(i2c)
i = 0
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
    
while True :
    [x,y,z] = acc.acceleration
    time.sleep(0.1)
    i = i + 1
    if i == 1:
        i = 0
        data = [x,y,z]
        print(data)
        lr = joblib.load('pig_earthquake.model')
        #Predict = lr.predict([np.array([-9.4928,0.196133,2.27513])])
        Predict = lr.predict([data])
        print('Predict : ', Predict)
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        