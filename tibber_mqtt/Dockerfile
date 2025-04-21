FROM python:3.11-alpine

RUN apk add --no-cache bash dos2unix && pip install gql paho-mqtt websockets

WORKDIR /app
COPY run.sh tibber.py ./

RUN dos2unix run.sh && chmod +x run.sh

CMD ["bash","run.sh"]
