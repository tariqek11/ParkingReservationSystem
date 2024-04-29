import paho.mqtt.client as mqtt
import json
import psycopg2
from psycopg2 import OperationalError
import os
import db
import requests
from datetime import datetime, timedelta, timezone

db_conn = db.create_connection()

BASE_URL = "http://127.0.0.1:8001"

# MQTT Server Parameters
MQTT_BROKER = "coe892.cloud.shiftr.io"
MQTT_PORT = 1883
MQTT_TOPIC = "parking"
MQTT_USER = "coe892"
MQTT_PASSWORD = "toknPZs4aU0s486V"

# Variables to store message parameters
parking_number = None
availability = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    global parking_number, availability
    payload = json.loads(msg.payload.decode())
    
    if 'Parking #' in payload and 'Availability' in payload:
        parking_number = payload['Parking #']
        availability = payload['Availability']
        print("Received message: ", payload)

        if(availability == "Occupied"):
            update_query = f"UPDATE parking_lot SET availability = FALSE WHERE space_id = {parking_number}"
        elif(availability == "Free"):
            update_query = f"UPDATE parking_lot SET availability = TRUE WHERE space_id = {parking_number}"
        db.execute_update_query(connection=db_conn, query=update_query)
    else:
        print("Invalid message format: ", payload)

    select = "SELECT * FROM parking_lot"
    results = db.execute_read_query(connection=db_conn, query=select)

    for result in results:
        print(result)



def main():
  
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to MQTT broker...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting from MQTT broker...")
        client.disconnect()
        db_conn.close()

if __name__ == "__main__":
    main()