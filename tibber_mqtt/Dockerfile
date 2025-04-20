FROM python:3.11-alpine

RUN pip install gql paho-mqtt websockets

COPY run.sh /run.sh
COPY tibber.py /tibber.py

RUN chmod +x /run.sh

CMD [ "/run.sh" ]
