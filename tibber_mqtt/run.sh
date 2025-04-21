#!/bin/bash

# Home Assistant maps UI fields into env vars:
# $TIBBER_TOKEN, $HOME_ID, $MQTT_HOST, $MQTT_PORT, $MQTT_USER, $MQTT_PASSWORD

exec python3 /app/tibber.py \
  "$TIBBER_TOKEN" \
  "$HOME_ID" \
  "$MQTT_HOST" \
  "$MQTT_PORT" \
  "$MQTT_USER" \
  "$MQTT_PASSWORD"
