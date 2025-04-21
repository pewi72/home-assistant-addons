#!/usr/bin/env python3
import sys

print("[TIBBER MQTT DEBUG] Script started")
print(f"[TIBBER MQTT DEBUG] Arguments: {sys.argv}")

TOKEN = sys.argv[1]
HOME_ID = sys.argv[2]
MQTT_HOST = sys.argv[3]
MQTT_PORT = int(sys.argv[4])
MQTT_USER = sys.argv[5]
MQTT_PASS = sys.argv[6]

print(f"[TIBBER MQTT DEBUG] Connecting to MQTT {MQTT_HOST}:{MQTT_PORT} as {MQTT_USER}")
# Placeholder for actual Tibber/MQTT logic
