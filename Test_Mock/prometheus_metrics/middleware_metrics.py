from prometheus_client import Counter, Histogram, CollectorRegistry, multiprocess
from prometheus_client.exposition import make_asgi_app
import time
from fastapi import Request
from loguru import logger
from starlette.concurrency import iterate_in_threadpool

# Определяем метрики
request_time_metrics = Histogram('custom_request_processing_seconds', 'Time spent processing request', ['endpoint'])
all_requests_metrics = Counter('all_requests', 'A counter of all requests made', ["endpoint"])


# Создаем функцию для создания приложения метрик
def make_metrics_app():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return make_asgi_app(registry=registry)



async def handler_middleware(request: Request, call_next):
    if request.url.path in ["/metrics", "/metrics/"]:
        # Skip processing for /metrics
        return await call_next(request)

    body = await request.body()
    body_str = body.decode("utf-8")
    logger.info(f"Request: {request.url} - {body_str} - {request.method}")
        
    # start_time = time.time()
    start_time = time.perf_counter()  # Используем time.perf_counter() вместо time.time()
    all_requests_metrics.labels(endpoint=request.url.path).inc()
    
    response = await call_next(request)

    response_body = [chunk async for chunk in response.body_iterator]
    response.body_iterator = iterate_in_threadpool(iter(response_body))
    logger.info(f"Response: {response.status_code} - {response_body[0].decode()}")
        
    # process_time = time.time() - start_time
    process_time = time.perf_counter() - start_time
    request_time_metrics.labels(endpoint=request.url.path).observe(process_time)
    return response