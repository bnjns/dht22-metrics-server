import os
import sys
import time
import adafruit_dht
import board
from loguru import logger
from prometheus_client import start_http_server, Gauge

def fetch_readings(dht_device, temperature_gauge, humidity_gauge):
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        logger.trace(f"Temperature = {temperature}. Humidity = {humidity}")

        temperature_gauge.set(temperature)
        humidity_gauge.set(humidity)
    except Exception as e:
        logger.error(f"Error reading temperature/humidity: {e}")

def main():
    logger.remove()
    logger.add(sys.stdout, level=os.environ.get("LOG_LEVEL", "info").upper(), format="ts=\"{time}\" level={level} msg=\"{message}\"")

    logger.debug("Creating Prometheus gauges")
    temperature = Gauge("dht22_temperature", "Temperature in Celsius")
    humidity = Gauge("dht22_humidity", "Humidity in percent")

    logger.debug("Initializing DHT22 sensor")
    dht_device = adafruit_dht.DHT22(board.D4)

    port = int(os.environ.get("PORT", 8000))
    start_http_server(port)
    logger.info(f"Server listening on :{port}")

    fetch_interval = int(os.environ.get("FETCH_INTERVAL", 5))
    logger.debug(f"Starting readings loop with interval: {fetch_interval}s")
    while True:
        logger.trace("Fetching readings from sensor")
        fetch_readings(dht_device, temperature, humidity)
        time.sleep(fetch_interval)

if __name__ == '__main__':
    main()
