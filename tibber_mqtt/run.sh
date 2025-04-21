#!/bin/bash
set -e

echo "[TIBBER MQTT] Starting addon..."

# Get configuration from options.json
CONFIG_PATH=/data/options.json

if [ -f "${CONFIG_PATH}" ]; then
    echo "[TIBBER MQTT] Loading configuration..."
    # Extract configuration values
    TIBBER_TOKEN=$(jq --raw-output '.tibber_token // empty' $CONFIG_PATH)
    HOME_ID=$(jq --raw-output '.home_id // empty' $CONFIG_PATH)
    MQTT_HOST=$(jq --raw-output '.mqtt_host // empty' $CONFIG_PATH)
    MQTT_PORT=$(jq --raw-output '.mqtt_port // empty' $CONFIG_PATH)
    MQTT_USER=$(jq --raw-output '.mqtt_user // empty' $CONFIG_PATH)
    MQTT_PASS=$(jq --raw-output '.mqtt_password // empty' $CONFIG_PATH)
    
    # Set defaults if values are empty
    MQTT_HOST=${MQTT_HOST:-"core-mosquitto"}
    MQTT_PORT=${MQTT_PORT:-1883}
    
    # Debug output (remove sensitive data for production)
    echo "[TIBBER MQTT] Configuration loaded."
    echo "[TIBBER MQTT] MQTT Host: $MQTT_HOST"
    echo "[TIBBER MQTT] MQTT Port: $MQTT_PORT"
    
    # Check required configuration
    if [ -z "$TIBBER_TOKEN" ]; then
        echo "[TIBBER MQTT ERROR] No Tibber token specified!"
        exit 1
    fi
    
    if [ -z "$HOME_ID" ]; then
        echo "[TIBBER MQTT ERROR] No Home ID specified!"
        exit 1
    fi
    
    # Start the application
    echo "[TIBBER MQTT] Starting the Tibber MQTT client..."
    python3 /app/tibber.py "$TIBBER_TOKEN" "$HOME_ID" "$MQTT_HOST" "$MQTT_PORT" "$MQTT_USER" "$MQTT_PASS"
else
    echo "[TIBBER MQTT ERROR] Configuration file not found!"
    exit 1
fi
