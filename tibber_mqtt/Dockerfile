FROM python:3.11-alpine

# Installera bashio-kompatibla verktyg (om vi använder bashio-syntax)
RUN apk add --no-cache bash curl jq dos2unix

# Installera Python-paket
RUN pip install gql paho-mqtt websockets

# Kopiera skript
COPY run.sh /run.sh
COPY tibber.py /tibber.py

# Säkerställ korrekt radslut och gör körbar
RUN dos2unix /run.sh && chmod +x /run.sh

CMD ["/run.sh"]
