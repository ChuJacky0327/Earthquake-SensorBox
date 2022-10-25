import random
import numpy as np
from paho.mqtt import client as mqtt_client
import csv

broker = 'broker.hivemq.com'
port = 1883
topic = "pig2"
topic_remove = "pigremove"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

def publish(client):
    
    #msg = 'Remove'
    msg = 'RandomRemove'
    result = client.publish(topic_remove, msg)
    # result: [0, 1]
    
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic_remove}`")
    else:
        print(f"Failed to send message to topic {topic_remove}")
        


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.username_pw_set('jacky','jacky')
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        mes = message.split("\n")
        #print(message)
        print(mes)
        print(mes[0])
        print(len(mes))
        #print(type(mes[0]))
        text = mes[0].split(",")
        
        
        with open('RandomEarthfile.csv', 'a', newline='') as csvfile:#newline='' 會多一筆資料是空格
            writer = csv.writer(csvfile)
            for i in range(0,len(mes)-1):
                text = mes[i].split(",")
                print(text)
                writer.writerow([text[0], text[1], text[2],text[3]])#random 5筆資料、另一個4筆
                print(text[0])
                print(text[1])
                print(text[2])
                print(text[3])
                
        
        publish(client)
        
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    #publish(client)
    client.loop_forever()


if __name__ == '__main__':
    run()