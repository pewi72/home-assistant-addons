FROM python:3.11-alpine

WORKDIR /app
COPY run.sh /run.sh
COPY tibber_mqtt.py /app/tibber_mqtt.py

RUN chmod a+x /run.sh \
    && pip install gql paho-mqtt websockets requests

CMD ["/run.sh"]
