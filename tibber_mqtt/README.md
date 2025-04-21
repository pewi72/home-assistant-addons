# Tibber MQTT Add-on

Detta Home Assistant add-on publicerar live Tibber-data till MQTT med Auto Discovery.

## Konfiguration

Ange din Tibber Access Token och Home ID i add-on-konfigurationen.

## Options

| Option   | Type   | Required | Description            |
|----------|--------|----------|------------------------|
| token    | string | true     | Din Tibber API token   |
| home_id  | string | true     | ID för ditt Tibber hem |

## MQTT

Add-on använder Home Assistants inbyggda MQTT-broker (`core-mosquitto`) med användare `mqtt` / `mqtt`.

## Usage

1. Installera och konfigurera add-on med din token och home_id.
2. Starta add-on.

Sensor publiceras under:
- `homeassistant/sensor/tibber_<home_id>_power/state`
Auto discovery konfig publiceras under:
- `homeassistant/sensor/tibber_<home_id>_power/config`

State JSON inkluderar:
```json
{
  "power": 123.45,
  "accumulatedConsumption": 12.34,
  "accumulatedProduction": 0.00
}
```