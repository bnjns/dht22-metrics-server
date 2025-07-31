# DHT22 Metrics Server for Raspberry Pi

A simple HTTP server that can be used to fetch the temperature (C) and humidity (%) from a DHT22 sensor attached to a
Raspberry Pi and expose them as Prometheus metrics.

To run natively:

- Consult [the Dockerfile](Dockerfile) on how to install the necessary system packages
- Install the Python packages with `pipenv install`
- Run the server: `python3 src/server.py`

Alternatively, run using Docker:

```
docker build -f dht22-metrics-server:latest .
docker run --rm -p 8000:8000 --privileged dht22-metrics-server:latest
```

Credit:

- <https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/>
