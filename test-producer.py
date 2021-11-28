from kafka import KafkaProducer
import pickle

producer = KafkaProducer(bootstrap_servers='10.0.0.14:9092', value_serializer=pickle.dumps)

for i in range(50):
    producer.send('topic-one', {'key': 'test'})
