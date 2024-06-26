from confluent_kafka import Consumer, Producer

# Настройки подключения к Kafka
conf = {
    'bootstrap.servers': 'localhost:9092',  # Замените на адрес вашего сервера Kafka
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

# Создание консьюмера для чтения из исходного топика
consumer = Consumer(conf)
consumer.subscribe(['Request'])  # Замените 'source_topic' на имя вашего исходного топика

# Создание продюсера для отправки в целевой топик
producer = Producer({'bootstrap.servers': 'localhost:9092'})  # Замените на адрес вашего сервера Kafka

while True:
    msg = consumer.poll(1.0)  # Чтение сообщений с задержкой в 1 секунду
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    # Отправка полученного сообщения в целевой топик
    producer.produce('Response', key=str("Response"), value=msg.value())  # Замените 'target_topic' на имя вашего целевого топика
    producer.flush()  # Ждем подтверждения отправки сообщения

consumer.close()
