from kafka import KafkaConsumer
import pickle
import numpy as np
import strlearn as sl
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from strlearn.metrics import precision
from strlearn.evaluators import TestThenTrain
import matplotlib.pyplot as plt

consumer = KafkaConsumer('topic-one',
                         group_id='adapter',
                         bootstrap_servers=['10.0.0.14:9092'],
                         value_deserializer=pickle.loads)

X = 0
y = 0
chunk_size = 500
n_chunks = 10

for msg in consumer:
    if isinstance(msg.value['Data'], np.ndarray):
        if msg.value['Data'].ndim == 2:
            X = msg.value['Data']
            # print('X')
        elif msg.value['Data'].ndim == 1:
            y = msg.value['Data']
            # print('y')
        else:
            print('Error: Incorrect number of dimensions')
    # elif isinstance(msg.value['y_array'], np.ndarray):
    #     if msg.value['y_array'].ndim == 1:
    #         y = msg
    #         print('y')
    #     else:
    #         print('Error: Incorrect number of dimensions')
    else:
        print("%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition,
                                             msg.offset, msg.key,
                                             msg.value))
        print(type(msg.value['Data']))
    if isinstance(X, np.ndarray) and isinstance(y, np.ndarray):
        break

print('stop')

np.save('merge', (np.concatenate((X, y[:, None]), axis=1)))
stream_new = sl.streams.NPYParser(path="merge.npy",
                                  chunk_size=chunk_size,
                                  n_chunks=n_chunks)

clf = GaussianNB()
metrics = [accuracy_score, precision]
evaluator = TestThenTrain(metrics)

evaluator.process(stream_new, clf)

np.save('analysis_results', evaluator.scores)

plt.figure(figsize=(6, 3))

for m, metric in enumerate(metrics):
    plt.plot(evaluator.scores[0, :, m], label=metric.__name__)

plt.title("Basic example of stream processing")
plt.ylim(0, 1)
plt.ylabel('Quality')
plt.xlabel('Chunk')

plt.legend()
plt.show()
