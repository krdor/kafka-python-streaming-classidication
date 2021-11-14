from kafka import KafkaConsumer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from strlearn.metrics import precision
from strlearn.evaluators import TestThenTrain

consumer = KafkaConsumer('topic',
                         bootstrap_servers='10.0.0.12:9092',
                         security_protocol='SASL_PLAINTEXT',
                         sasl_mechanism='PLAIN',
                         sasl_plain_username='user',
                         sasl_plain_password='iZcWS33fJQML')
for msg in consumer:
    print(msg)

#how to build a sream out of this? ^

clf = GaussianNB()
metrics = [accuracy_score, precision()]
evaluator = TestThenTrain(metrics)

evaluator.process(stream, clf)

#zapis do pliku?
