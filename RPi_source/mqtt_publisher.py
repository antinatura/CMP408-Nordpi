"""
Name: mqtt_publisher.py
Desc: send CSV to server via MQTT
Auth: Ance Strazdina
Date: 11/12/2023
"""

# imports
import paho.mqtt.client as mqtt 
import socket, sys

# MQTT details
broker = '' # Elastic IP of the EC2 instance
user = '' # username here
passwd = '' # password here
topic = 'pi/elspot'

# read in the CSV file content
try:
    with open('elspot.csv', 'r') as file:
        csv_content = file.read()
except FileNotFoundError::
    sys.exit("Couldn't find elspot.csv.")

# create client and connect
client = mqtt.Client() 
client.username_pw_set(user, passwd) 
try:
    client.connect(broker)
except socket.timeout:
    sys.exit("Couldn't establish connection to the broker.")

# publish data
client.publish(topic, csv_content)
client.disconnect()
