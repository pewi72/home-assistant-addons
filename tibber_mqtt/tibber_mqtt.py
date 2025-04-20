import os
import asyncio
import json
import ssl
import paho.mqtt.client as mqtt
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

MQTT_DISCOVERY_PREFIX = "homeassistant"

FIELDS = {
    "power": "Power",
    "accumulatedConsumption": "Accumulated Consumption",
    "accumulatedProduction": "Accumulated Production",
    "accumulatedCost": "Accumulated Cost",
    "accumulatedReward": "Accumulated Reward",
    "minPower": "Min Power",
    "averagePower": "Average Power",
    "maxPower": "Max Power",
    "powerProduction": "Power Production",
    "voltagePhase1": "Voltage Phase 1",
    "voltagePhase2": "Voltage Phase 2",
    "voltagePhase3": "Voltage Phase 3",
    "currentL1": "Current L1",
    "currentL2": "Current L2",
    "currentL3": "Current L3",
    "signalStrength": "Signal Strength"
}

options = {
    "tibber_token": os.getenv("TIBBER_TOKEN", ""),
    "home_id": os.getenv("HOME_ID", ""),
    "mqtt_host": os.getenv("MQTT_HOST", "core-mosquitto"),
    "mqtt_port": int(os.getenv("MQTT_PORT", 1883)),
    "mqtt_user": os.getenv("MQTT_USER", ""),
    "mqtt_password": os.getenv("MQTT_PASSWORD", "")
}

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(options["mqtt_user"], options["mqtt_password"])
mqtt_client.connect(options["mqtt_host"], options["mqtt_port"])
mqtt_client.loop_start()

async def main():
    query = gql("""
    subscription {
      liveMeasurement(homeId: \"%s\") {
        timestamp
        %s
      }
    }
    """ % (options["home_id"], "\n        ".join(FIELDS.keys())))

    transport = WebsocketsTransport(
        url="wss://api.tibber.com/v1-beta/gql/subscriptions",
        headers={"Authorization": f"Bearer {options['tibber_token']}"},
        ssl=ssl.create_default_context()
    )

    async with Client(transport=transport, fetch_schema_from_transport=False) as session:
        async for result in session.subscribe(query):
            data = result["liveMeasurement"]
            for field, friendly_name in FIELDS.items():
                if field in data:
                    value = data[field]
                    object_id = f"tibber_{field.lower()}"
                    topic = f"{MQTT_DISCOVERY_PREFIX}/sensor/{object_id}/config"
                    state_topic = f"tibber/{object_id}/state"
                    payload = {
                        "name": friendly_name,
                        "state_topic": state_topic,
                        "unit_of_measurement": "",
                        "unique_id": object_id,
                        "device": {
                            "identifiers": ["tibber_sensor"],
                            "name": "Tibber Sensors",
                            "manufacturer": "Tibber"
                        }
                    }
                    mqtt_client.publish(topic, json.dumps(payload), retain=True)
                    mqtt_client.publish(state_topic, value, retain=True)

if __name__ == "__main__":
    asyncio.run(main())
