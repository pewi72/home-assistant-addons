#!/bin/bash

echo "[TIBBER MQTT DEBUG] Starting add-on..."

if [ -z "${TIBBER_TOKEN}" ] || [ -z "${HOME_ID}" ]; then
  echo "[TIBBER MQTT ERROR] Missing required environment variables"
  exit 1
fi

echo "[TIBBER MQTT DEBUG] Environment variables:"
echo "TIBBER_TOKEN=${TIBBER_TOKEN:0:5}..."
echo "HOME_ID=${HOME_ID}"
echo "MQTT_HOST=${MQTT_HOST}"
echo "MQTT_PORT=${MQTT_PORT}"
echo "MQTT_USER=${MQTT_USER}"

python3 /app/tibber.py "${TIBBER_TOKEN}" "${HOME_ID}" "${MQTT_HOST}" "${MQTT_PORT}" "${MQTT_USER}" "${MQTT_PASSWORD}"
