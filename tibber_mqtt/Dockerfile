FROM python:3.11-alpine

RUN apk add --no-cache bash curl jq dos2unix

RUN pip install gql paho-mqtt websockets

# Skapa arbetskatalog och kopiera filer
WORKDIR /app
COPY run.sh .
COPY tibber.py .

# Fix radslut och rättigheter
RUN dos2unix run.sh && chmod +x run.sh

CMD [ "bash", "/app/run.sh" ]
