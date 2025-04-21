FROM python:3.11-alpine

RUN apk add --no-cache bash curl jq dos2unix

RUN pip install gql paho-mqtt websockets

WORKDIR /app
COPY run.sh /app/
COPY tibber.py /app/

RUN chmod +x /app/run.sh
RUN chmod +x /app/tibber.py
RUN dos2unix /app/run.sh

CMD [ "bash", "/app/run.sh" ]
