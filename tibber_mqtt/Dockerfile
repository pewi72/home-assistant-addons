ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip bash curl && \
    rm -rf /var/lib/apt/lists/*

# Copy root filesystem and scripts
COPY rootfs /

# Copy application
COPY tibber_mqtt /usr/src/tibber_mqtt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /usr/src/tibber_mqtt/requirements.txt

CMD ["/init"]
