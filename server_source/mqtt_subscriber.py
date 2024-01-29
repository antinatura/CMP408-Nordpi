"""
Name: mqtt_subscriber.py
Desc: susbscribe to the elspot topic and get data sent from RPi via MQTT
Auth: Ance Strazdina
Date: 11/12/2023
"""

# imports
import paho.mqtt.client as mqtt

# MQTT details
broker = '' # Elastic IP of the EC2 instance
user = '' # username here
passwd = '' # password here
topic = 'pi/elspot'

# callback function when a message is received
def on_message(client, userdata, msg):
    csv_content = msg.payload.decode()
    # save the CSV content to a file
    with open('/home/ubuntu/nordpool_scrape/elspot.csv', 'w') as file:
        file.write(csv_content)

client = mqtt.Client() # create client
client.on_message = on_message # callback function on message

# connect
client.username_pw_set(user, passwd) 
client.connect(broker) 

client.subscribe(topic) # subscribe to the topic
client.loop_forever()