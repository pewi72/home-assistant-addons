# Tibber MQTT Home Assistant Add-on

Detta tillägg hämtar realtidsdata från Tibber (liveMeasurement) och publicerar den till MQTT med Home Assistant autodiscovery.

## Installation
1. Lägg till denna repo i Home Assistant som en lokal add-on:
   `https://github.com/pewi72/home-assistant-addons`
2. Konfigurera:
   - `tibber_token`: Din personliga Tibber API-token
   - `home_id`: Ditt Home-ID från Tibber
   - MQTT-inställningar: host, port, användarnamn och lösenord
3. Starta tillägget – sensorerna skapas automatiskt i Home Assistant

## Sensordata
Tillägget skapar en sensor per fält från `liveMeasurement`, t.ex.:
- `sensor.tibber_power`
- `sensor.tibber_accumulated_consumption`
- `sensor.tibber_voltage_phase1`

Autodiscovery gör att sensorerna dyker upp automatiskt i Home Assistant.
