#!/usr/bin/env python3
import sys
import time
import paho.mqtt.client as mqtt
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

print("[TIBBER MQTT] Script started")
print(f"[TIBBER MQTT] Arguments: {sys.argv}")

if len(sys.argv) != 7:
    print("[TIBBER MQTT] ERROR: Expected 6 args: token, home_id, host, port, user, pass")
    sys.exit(1)

TOKEN, HOME_ID, MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASS = sys.argv[1:]

print(f"[TIBBER MQTT] Connecting to MQTT {MQTT_HOST}:{MQTT_PORT} as {MQTT_USER}")
client = mqtt.Client("tibber-client")
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_HOST, int(MQTT_PORT), 60)

# TODO: Implement Tibber GraphQL subscription and publish to MQTT
while True:
    payload = f"heartbeat: {int(time.time())}"
    client.publish("tibber/heartbeat", payload)
    print(f"[TIBBER MQTT] Published: {payload}")
    time.sleep(60)
