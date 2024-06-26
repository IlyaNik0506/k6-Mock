import json
# import asyncio
import aiofiles
from prometheus_client import Gauge

# Определите пользовательскую метрику для хранения задержки для каждой конечной точки
endpoint_delay = Gauge("endpoint_delay_seconds", "Задержка в секундах для каждой конечной точки", ["endpoint"])

async def load_endpoints(name):
    async with aiofiles.open('config_endpoints.json', 'r') as file:
        config_str = await file.read()

    config = json.loads(config_str)

    for item in config:
        if item['name'] == name:
            delay = item['delay']
            endpoint_delay.labels(name).set(delay)
            return delay

    raise ValueError(f"Конечная точка '{name}' не найдена")