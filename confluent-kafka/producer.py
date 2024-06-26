import time
from confluent_kafka import Producer
import random

# Настройка подключения к Kafka
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def send_message():
    # Генерация случайного MsgId
    msg_id = random.randint(1000, 9999)
    
    # Формирование сообщения с текущей датой и MsgId
    message = f"Дата: {time.strftime('%Y-%m-%d %H:%M:%S')}, MsgId: {msg_id}"
    
    # Отправка сообщения
    producer.produce('Request', message.encode('utf-8'), key=str("Request"))
    # producer.produce('Request', message.encode('utf-8'), key=str("Request-1"))
    print(f"Отправлено сообщение: {message}")

while True:
    send_message()
    time.sleep(2)  # Пауза перед следующим отправлением сообщения
