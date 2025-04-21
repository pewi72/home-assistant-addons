#!/usr/bin/env python3
import sys
import time
import paho.mqtt.client as mqtt

print("[TIBBER MQTT DEBUG] Script started")

if len(sys.argv) < 7:
    print("[TIBBER MQTT ERROR] Missing arguments")
    print(f"[TIBBER MQTT DEBUG] Received arguments: {sys.argv}")
    sys.exit(1)

TOKEN = sys.argv[1]
HOME_ID = sys.argv[2]
MQTT_HOST = sys.argv[3]
MQTT_PORT = int(sys.argv[4])
MQTT_USER = sys.argv[5]
MQTT_PASS = sys.argv[6]

print(f"[TIBBER MQTT DEBUG] Connecting to MQTT {MQTT_HOST}:{MQTT_PORT} as {MQTT_USER}")

try:
    client = mqtt.Client("tibber-client")
    if MQTT_USER and MQTT_PASS:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    print("[TIBBER MQTT DEBUG] MQTT connection successful")
    client.publish("tibber/status", "online")
    print("[TIBBER MQTT DEBUG] Published test message")
    while True:
        client.publish("tibber/heartbeat", str(time.time()))
        time.sleep(60)
except Exception as e:
    print(f"[TIBBER MQTT ERROR] {str(e)}")
    sys.exit(1)
