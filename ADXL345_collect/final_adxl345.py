# ADXL345 Python library for Raspberry Pi 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer
#!/usr/bin/python3
import smbus
import time
import RPi.GPIO as GPIO
from time import sleep
import math
from datetime import datetime
import random
from paho.mqtt import client as mqtt_client
import json  
import socket
import os
REMOTE_SERVER = "www.google.com"
broker = 'broker.hivemq.com'
port = 1883
topic = "CHU"
topic_PC = "pig"
topic_PC2 = "pig2"
topic_remove = "pigremove"
message_remove = "noRemove"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.OUT)

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set("jacky","jacky")
    client.connect(broker, port)
    return client


def publish(client,text,topic_name):
    msg_count = 0     
    #msg = f"messages: {msg_count}\n{text}"
    msg = text
    result = client.publish(topic_name, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_name}`")
    else:
        print(f"Failed to send message to topic {topic_name}")
    msg_count += 1
    #time.sleep(100)

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        global message_remove 
        message_remove = msg.payload.decode()
        print(message_remove)
        print("ok")
        #client.disconnect
        #print("ok")
        #return message_remove

    client.subscribe(topic_remove)
    client.on_message = on_message
    



def run():    
    
    global message_remove
    internet_count = 0
    mqtt_count = 0
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
    random_original = adxl345.getAxes(True)
    f= open("earthfile.txt",'a')
    

    while True:
        if __name__ == "__main__":
            adxl345 = ADXL345()
            axes = adxl345.getAxes(True)
            axes_random = adxl345.getAxes(True)
            #print ("ADXL345 on address 0x%x:" % (adxl345.address))
            random_x = axes_random['x']-random_original['x']
            random_y = axes_random['y']-random_original['y']
            random_z = axes_random['z']-random_original['z']
            random_x = round(random_x,3)
            random_y = round(random_y,3)
            random_z = round(random_z,3)
            print ("ADXL345 on address 0x%x:" % (adxl345.address))
            #print (random_original['x'])
            #print (random_original['y'])
            #print (random_original['z'])
            print ("   random_x = %.3fG" % ( random_x ))
            print ("   random_y = %.3fG" % ( random_y ))
            print ("   random_z = %.3fG" % ( random_z ))
            if((abs(random_x) >0.05) or (abs(random_y) >0.05) or (abs(random_z) >0.05)):
                with open("random_earthfile.txt",'a') as s :
                     s.write(str(datetime.now())+' ,random_x='+ str(random_x)+' ,random_y='+ str(random_y) +' ,random_z='+ str(random_z)+'\n')
                     #jump.Z()
                     s.flush()
                     print("OK")
                     #f.close()
                     #break
                     
            if ((abs(axes['x'] - original['x']) >= 0.1) or (abs(axes['y'] - original['y']) >= 0.1) or (abs(axes['z'] - original['z']) >= 0.1) ):#0.1  
                #print ("   x = %.3fG" % ( axes['x'] - original['x']))
                #print ("   y = %.3fG" % ( axes['y'] - original['y']))
                #print( "   z = %.3fG" % ( axes['z'] - original['z']))
                ax = axes['x'] - original['x']
                ay = axes['y'] - original['y']
                az = axes['z'] - original['z']
                ax = round(ax,3)
                ay = round(ay,3)
                az = round(az,3)
                #aI = math.sqrt( ax*ax + ay*ay + az*az )
                #aI = aI*20
                #print(aI)
                #I = (math.log(aI,10) + 0.7)*2
                #print('I:'+str(I))
                #print('intensity : ' +str(int(I)))
                try:
                     client = connect_mqtt()
                     #client.loop_start()
                     publish(client, str(datetime.now())+' ,ax='+ str(ax)+' ,ay='+ str(ay) +' ,az='+ str(az),topic)
                     with open("earthfile.txt",'a') as f :
                         f.write(str(datetime.now())+' ,ax='+ str(ax)+' ,ay='+ str(ay) +' ,az='+ str(az)+'\n')
                         #jump.Z()
                         f.flush()
                         #f.close()
                         #break
                except:
                     with open("earthfile.txt",'a') as f :
                         f.write(str(datetime.now())+' ,ax='+ str(ax)+' ,ay='+ str(ay) +' ,az='+ str(az)+'\n')
                         #jump.Z()
                         f.flush()
                         #f.close()
                         #break
                #time.sleep(1)
                original = adxl345.getAxes(True)
                continue
            else: 
                #print ("   x = %.3fG" % ( axes['x'] - original['x']))
                #print ("   y = %.3fG" % ( axes['y'] - original['y']))
                #print ("   z = %.3fG" % ( axes['z'] - original['z']))
                pass
                
                
            internet_count = internet_count + 1
            mqtt_count = mqtt_count + 1
            if internet_count == 5:
                try :
                    host = socket.gethostbyname(REMOTE_SERVER)
                    s = socket.create_connection((host,80),2)
                    GPIO.output(25,GPIO.LOW)
                    print('internet_yes')
                except :
                    GPIO.output(25,GPIO.HIGH)
                    print('internet_no')
                internet_count = 0
                
            if mqtt_count == 5000:
                try :
                    with open("earthfile.txt",'r') as f :
                        earthfile_txt = f.read()
                    with open("random_earthfile.txt",'r') as s :
                        random_earthfile_txt = s.read()   
                    client = connect_mqtt()
                    #client.loop_start()
                    publish(client,str(earthfile_txt),topic_PC)
                    publish(client,str(random_earthfile_txt),topic_PC2)
                    print('mqtt_send_txt')
                except :
                    print('mqtt_send_error')
                mqtt_count = 0
            
            try:    
                random_file = r'/home/pi/Desktop/adxl345/random_earthfile.txt'
                random_file_size = os.path.getsize(r'/home/pi/Desktop/adxl345/random_earthfile.txt')
                print('message_remove :' + message_remove)
                if random_file_size > 1000 :#byte
                    host = socket.gethostbyname(REMOTE_SERVER)
                    s = socket.create_connection((host,80),2)
                    with open("random_earthfile.txt",'r') as s :
                        random_earthfile_txt = s.read()   
                    client = connect_mqtt()
                    publish(client,str(random_earthfile_txt),topic_PC2)
                    print('mqtt_send_txt')
                    subscribe(client)
                    client.loop_start()
                    time.sleep(5)
                    print('message_remove :' + message_remove)
                    if message_remove == "RandomRemove" :
                        os.remove (random_file)
                        print("random_earthfile.txt is remove")
                        message_remove = "noRemove"
                    else :
                        print("no recive message")
                    
                    
                    
                file = r'/home/pi/Desktop/adxl345/earthfile.txt'
                file_size = os.path.getsize(r'/home/pi/Desktop/adxl345/earthfile.txt')
                if file_size > 1000 :#byte
                    host = socket.gethostbyname(REMOTE_SERVER)
                    s = socket.create_connection((host,80),2)
                    with open("earthfile.txt",'r') as f :
                        earthfile_txt = f.read()   
                    client = connect_mqtt()
                    publish(client,str(earthfile_txt),topic_PC)
                    print('mqtt_send_txt')
                    subscribe(client)
                    client.loop_start()
                    time.sleep(5)
                    print('message_remove :' + message_remove)
                    if message_remove == "Remove" :
                        os.remove (file)
                        print("earthfile.txt is remove")
                        message_remove = "noRemove"
                    else :
                        print("no recive message")
            except :
                print('no file remove')
            time.sleep(0.5)
            
            
run()
