import os
import asyncio
import psutil
from prometheus_client import Gauge

# Создаем метрики для ЦПУ и памяти
cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
memory_usage = Gauge('memory_usage_percent', 'Memory usage percentage')

# Функция для обновления метрик ЦПУ и памяти
async def update_metrics():
    pid = os.getpid() # Получаем PID текущего процесса
    process = psutil.Process(pid) # Создаем объект процесса
    while True:
        cpu_usage.set(process.cpu_percent()) # Измеряем утилизацию ЦПУ процесса
        memory_usage.set(process.memory_percent()) # Измеряем утилизацию памяти процесса
        await asyncio.sleep(5) # Обновляем метрики каждые 10 секунд