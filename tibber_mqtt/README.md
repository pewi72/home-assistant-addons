# Tibber MQTT Home Assistant Add-on

Ett Home Assistant-tillägg som ansluter till Tibbers GraphQL API och publicerar realtidsdata (`liveMeasurement`) till MQTT. Sensordata visas automatiskt i Home Assistant via MQTT discovery.

## Funktioner

- 🔌 Prenumererar på `liveMeasurement` via WebSocket
- 📤 Publicerar till MQTT (ex: power, voltagePhase1, signalStrength)
- 🧠 Autodiscovery för Home Assistant-sensorer
- 🛠 Konfiguration via Add-on GUI (ingen hårdkodning)

## Installation

1. Lägg till denna repository i Home Assistant:
   ```
   https://github.com/pewi72/home-assistant-addons
   ```

2. Installera `Tibber MQTT`-tillägget via GUI.

3. Ange följande i konfigurationen:
   - `tibber_token`: Din Tibber API-token
   - `home_id`: ID för ditt hem (från Tibber API)
   - `mqtt_host`, `mqtt_port`, `mqtt_user`, `mqtt_password`: MQTT-inställningar

4. Starta tillägget. Sensordata bör dyka upp automatiskt i Home Assistant.

## Exempel på sensorer

- `sensor.tibber_power`
- `sensor.tibber_accumulated_consumption`
- `sensor.tibber_voltage_phase1`

## Licens

MIT