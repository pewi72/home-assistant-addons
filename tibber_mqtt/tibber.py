import sys
import asyncio
import json
import time
import ssl
import paho.mqtt.client as mqtt
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

# Debug output arguments
print("[TIBBER MQTT DEBUG] Script started")
print(f"[TIBBER MQTT DEBUG] Arguments: {sys.argv}")

# Ensure we have all required arguments
if len(sys.argv) < 5:
    print("[TIBBER MQTT ERROR] Not enough arguments provided")
    print("Usage: python3 tibber.py TIBBER_TOKEN HOME_ID MQTT_HOST MQTT_PORT [MQTT_USER] [MQTT_PASS]")
    sys.exit(1)

TIBBER_TOKEN = sys.argv[1]
HOME_ID = sys.argv[2]
MQTT_HOST = sys.argv[3]

# Handle potential empty string for MQTT_PORT
try:
    MQTT_PORT = int(sys.argv[4]) if sys.argv[4] else 1883
except ValueError:
    print(f"[TIBBER MQTT WARNING] Invalid MQTT port: '{sys.argv[4]}', using default 1883")
    MQTT_PORT = 1883

# Optional MQTT credentials
MQTT_USER = sys.argv[5] if len(sys.argv) > 5 else ""
MQTT_PASS = sys.argv[6] if len(sys.argv) > 6 else ""

MQTT_PREFIX = "homeassistant/sensor/tibber"

SENSOR_FIELDS = [
    "power",
    "accumulatedConsumption",
    "accumulatedProduction",
    "accumulatedCost",
    "minPower",
    "averagePower",
    "maxPower",
    "powerProduction",
    "powerReactive",
    "voltagePhase1",
    "voltagePhase2",
    "voltagePhase3",
    "currentL1",
    "currentL2",
    "currentL3",
    "signalStrength"
]

# Map for device classes and units
FIELD_PROPERTIES = {
    "power": {"device_class": "power", "unit": "W"},
    "powerProduction": {"device_class": "power", "unit": "W"},
    "powerReactive": {"device_class": "reactive_power", "unit": "VAR"},
    "accumulatedConsumption": {"device_class": "energy", "unit": "kWh"},
    "accumulatedProduction": {"device_class": "energy", "unit": "kWh"},
    "accumulatedCost": {"device_class": "monetary", "unit": "SEK"},
    "minPower": {"device_class": "power", "unit": "W"},
    "averagePower": {"device_class": "power", "unit": "W"},
    "maxPower": {"device_class": "power", "unit": "W"},
    "voltagePhase1": {"device_class": "voltage", "unit": "V"},
    "voltagePhase2": {"device_class": "voltage", "unit": "V"},
    "voltagePhase3": {"device_class": "voltage", "unit": "V"},
    "currentL1": {"device_class": "current", "unit": "A"},
    "currentL2": {"device_class": "current", "unit": "A"},
    "currentL3": {"device_class": "current", "unit": "A"},
    "signalStrength": {"device_class": "signal_strength", "unit": "dBm"}
}

def connect_mqtt():
    print(f"[TIBBER MQTT] Connecting to MQTT broker {MQTT_HOST}:{MQTT_PORT}")
    mqtt_client = mqtt.Client()
    
    if MQTT_USER and MQTT_PASS:
        mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
    
    try:
        mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
        mqtt_client.loop_start()
        print("[TIBBER MQTT] Successfully connected to MQTT broker")
        return mqtt_client
    except Exception as e:
        print(f"[TIBBER MQTT ERROR] Failed to connect to MQTT broker: {e}")
        return None

def publish_discovery(mqtt_client, field):
    if field not in FIELD_PROPERTIES:
        props = {"device_class": "power", "unit": "W"}
    else:
        props = FIELD_PROPERTIES[field]
    
    topic = f"{MQTT_PREFIX}/{field}/config"
    payload = {
        "name": f"Tibber {field}",
        "state_topic": f"{MQTT_PREFIX}/{field}/state",
        "unique_id": f"tibber_{field}",
        "device_class": props["device_class"],
        "unit_of_measurement": props["unit"],
        "device": {
            "identifiers": ["tibber_device"],
            "manufacturer": "Tibber",
            "model": "API",
            "name": "Tibber Energy Monitor"
        }
    }
    mqtt_client.publish(topic, json.dumps(payload), retain=True)
    print(f"[TIBBER MQTT] Published discovery for {field}")

def publish_state(mqtt_client, field, value):
    topic = f"{MQTT_PREFIX}/{field}/state"
    mqtt_client.publish(topic, value)

async def main():
    print(f"[TIBBER MQTT] Starting Tibber WebSocket for home {HOME_ID}...")
    
    mqtt_client = connect_mqtt()
    if not mqtt_client:
        print("[TIBBER MQTT ERROR] Failed to start MQTT client, exiting")
        return
    
    # Register all sensor entities with Home Assistant
    for field in SENSOR_FIELDS:
        publish_discovery(mqtt_client, field)
    
    # Set up the GQL client
    try:
        transport = WebsocketsTransport(
            url='wss://api.tibber.com/v1-beta/gql/subscriptions',
            init_payload={"token": TIBBER_TOKEN},
            ssl=ssl.create_default_context()
        )

        client = Client(transport=transport, fetch_schema_from_transport=False)

        query = gql(f"""
        subscription {{
          liveMeasurement(homeId: "{HOME_ID}") {{
            timestamp
            {" ".join(SENSOR_FIELDS)}
          }}
        }}
        """)
        
        print("[TIBBER MQTT] Starting subscription...")
        
        async with client as session:
            counter = 0
            async for result in session.subscribe(query):
                counter += 1
                if counter % 10 == 0:  # Log only every 10th update to reduce spam
                    print(f"[TIBBER MQTT] Received update #{counter}")
                
                measurement = result["liveMeasurement"]
                timestamp = measurement.get("timestamp")
                
                for field in SENSOR_FIELDS:
                    value = measurement.get(field)
                    if value is not None:
                        publish_state(mqtt_client, field, value)
    
    except Exception as e:
        print(f"[TIBBER MQTT ERROR] Error in subscription: {e}")
        
    finally:
        if mqtt_client:
            mqtt_client.loop_stop()
            mqtt_client.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[TIBBER MQTT] Addon stopped by user")
    except Exception as e:
        print(f"[TIBBER MQTT ERROR] Unexpected error: {e}")
