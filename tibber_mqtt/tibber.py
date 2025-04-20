import sys
import asyncio
import json
import time
import ssl
import paho.mqtt.client as mqtt
from gql import gql, Client
from gql.transport.websockets import WebsocketsTransport

TIBBER_TOKEN = sys.argv[1]
HOME_ID = sys.argv[2]
MQTT_HOST = sys.argv[3]
MQTT_PORT = int(sys.argv[4])
MQTT_USER = sys.argv[5]
MQTT_PASS = sys.argv[6]

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

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)
mqtt_client.loop_start()

def publish_discovery(field):
    topic = f"{MQTT_PREFIX}/{field}/config"
    payload = {
        "name": f"Tibber {field}",
        "state_topic": f"{MQTT_PREFIX}/{field}/state",
        "unique_id": f"tibber_{field}",
        "device_class": "power" if "power" in field else "energy",
        "unit_of_measurement": "W" if "power" in field else "kWh",
        "device": {
            "identifiers": ["tibber_device"],
            "manufacturer": "Tibber",
            "model": "Pulse",
            "name": "Tibber Pulse"
        }
    }
    mqtt_client.publish(topic, json.dumps(payload), retain=True)

def publish_state(field, value):
    topic = f"{MQTT_PREFIX}/{field}/state"
    mqtt_client.publish(topic, value)

async def main():
    print("🚀 Startar Tibber WebSocket...")

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

    for field in SENSOR_FIELDS:
        publish_discovery(field)

    async with client as session:
        async for result in session.subscribe(query):
            measurement = result["liveMeasurement"]
            for field in SENSOR_FIELDS:
                value = measurement.get(field)
                if value is not None:
                    publish_state(field, value)

if __name__ == "__main__":
    asyncio.run(main())
