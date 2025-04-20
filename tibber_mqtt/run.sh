#!/usr/bin/with-contenv bashio

TOKEN=$(bashio::config 'tibber_token')
HOME_ID=$(bashio::config 'home_id')
MQTT_HOST=$(bashio::config 'mqtt_host')
MQTT_PORT=$(bashio::config 'mqtt_port')
MQTT_USER=$(bashio::config 'mqtt_user')
MQTT_PASS=$(bashio::config 'mqtt_password')

python3 /tibber.py "$TOKEN" "$HOME_ID" "$MQTT_HOST" "$MQTT_PORT" "$MQTT_USER" "$MQTT_PASS"
