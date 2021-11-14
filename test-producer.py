from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='10.0.0.12:9092',
                         security_protocol='SASL_PLAINTEXT',
                         sasl_mechanism='PLAIN',
                         sasl_plain_username='user',
                         sasl_plain_password='iZcWS33fJQML'
                         )
for i in range(100):
    producer.send('topic', i.to_bytes(1, byteorder='big'))
