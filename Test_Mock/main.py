import os
import asyncio
from loguru import logger
from fastapi import FastAPI, Request, BackgroundTasks
from prometheus_client import Counter, Histogram, CollectorRegistry, multiprocess, Gauge

from fastapi import HTTPException
from starlette.responses import JSONResponse

from prometheus_metrics.middleware_metrics import make_metrics_app, handler_middleware

from prometheus_metrics.cpu_ram_metrics import update_metrics

import uvicorn
import time

from endpoints.MIG_1 import mig_1
from endpoints.MIG_2 import mig_2


# from prometheus_fastapi_instrumentator import Instrumentator

# Создаем основное приложение FastAPI
app = FastAPI()

# Инициализация Loguru
# Добавляем обработчик логов с именем файла, включающим текущую дату, и обновляем файл каждый день в 00:00
logger.add("logs/{time:YYYY-MM-DD}.log", rotation="00:02", level="INFO")
logger.add("sys.stderr", level="INFO") # Логи в консоль

# Устанавливаем переменную окружения PROMETHEUS_MULTIPROC_DIR
os.environ["PROMETHEUS_MULTIPROC_DIR"] = "prometheus_multiproc_dir"

# Создаем директорию, если она не существует
os.makedirs(os.environ["PROMETHEUS_MULTIPROC_DIR"], exist_ok=True)

# Обработка всех исключений на уровне сервера и промежуточного ПО
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Посмотри логи, происходит ДИЧЬ"},
    )

# монтируем приложение метрик Middleware
metrics_app = make_metrics_app()
app.mount("/metrics", metrics_app)

# Middleware для измерения времени обработки запросов и подсчета общего количества запросов
@app.middleware("http")
async def add_process_time_header_middleware(request: Request, call_next):
    return await handler_middleware(request, call_next)

@app.post("/RReq")
async def mig():
    return await mig_1()

@app.post("/AReq")
async def mig(request: Request):
    return await mig_2()

# Функция для запуска фонового процесса обновления метрик CPU-RAM
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_metrics())

# # Подключаем инструментатор Prometheus
# instrumentator = Instrumentator().instrument(app)
    
# # Экспонируем метрики Prometheus
# instrumentator.expose(app, include_in_schema=False)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, workers=1, log_level="info")
