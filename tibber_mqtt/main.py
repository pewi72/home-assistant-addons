import argparse
import asyncio
import json
import bashio
import tibber
import aiohttp
import paho.mqtt.client as mqtt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True, help='Tibber API token')
    parser.add_argument('--home-id', required=True, help='Tibber Home ID')
    return parser.parse_args()

def setup_mqtt():
    mqtt_config = {
        'host': bashio.config.get('mqtt.server'),
        'user': bashio.config.get('mqtt.user'),
        'password': bashio.config.get('mqtt.password')
    }
    client = mqtt.Client()
    client.username_pw_set(mqtt_config['user'], mqtt_config['password'])
    client.connect(mqtt_config['host'], 1883)
    client.loop_start()
    return client

async def main():
    args = parse_args()
    mqtt_client = setup_mqtt()

    async with aiohttp.ClientSession() as session:
        tibber_connection = tibber.Tibber(args.token, websession=session, user_agent="homeassistant-addon")
        await tibber_connection.update_info()
        home = tibber_connection.get_homes()[0]

        # Autodiscovery config
        state_topic = f"homeassistant/sensor/tibber_{args.home_id}_power/state"
        config_topic = f"homeassistant/sensor/tibber_{args.home_id}_power/config"
        config_payload = {
            "name": "Tibber Live Power",
            "state_topic": state_topic,
            "unit_of_measurement": "W",
            "value_template": "{{ value_json.power }}",
            "unique_id": f"tibber_{args.home_id}_power",
            "device": {
                "identifiers": [args.home_id],
                "name": "Tibber Home",
                "model": "Tibber API",
                "manufacturer": "Tibber"
            }
        }
        mqtt_client.publish(config_topic, json.dumps(config_payload), retain=True)

        # Live subscription callback
        def _callback(pkg):
            data = pkg.get('data', {}).get('liveMeasurement', {})
            mqtt_client.publish(state_topic, json.dumps(data))

        # Start live feed
        await home.rt_subscribe(_callback)

        # Keep running
        while True:
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())
