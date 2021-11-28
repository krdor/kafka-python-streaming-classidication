from kafka import KafkaConsumer
import pickle
import numpy as np
import strlearn as sl
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from strlearn.metrics import precision
from strlearn.evaluators import TestThenTrain

consumer = KafkaConsumer('topic-one',
                         group_id='adapter',
                         bootstrap_servers=['10.0.0.14:9092'],
                         value_deserializer=pickle.loads)

X = 0
y = 0

for msg in consumer:
    if isinstance(msg.value['X_array'], np.ndarray):
        print('slownik')
        if msg.value['X_array'].ndim == 2:
            X = msg
            print('X')
        elif msg.value['X_array'].ndim == 1:
            y = msg
            print('y')
        else:
            print('Error: Incorrect number of dimensions')
    else:
        print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value))
        print(type(msg.value['X_array']))
    if X and y:
        break

print('stop')

# how to build a stream out of this? ^
# stream = ?

# clf = GaussianNB()
# metrics = [accuracy_score, precision]
# evaluator = TestThenTrain(metrics)
#
# evaluator.process(stream, clf)

# zapis do pliku?
