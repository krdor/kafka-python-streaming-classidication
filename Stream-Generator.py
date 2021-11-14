import strlearn as sl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from kafka import KafkaProducer

n_chunks = 100

stream = sl.streams.StreamGenerator(
    weights=[0.3, 0.7],
    random_state=1407,
    n_chunks=n_chunks,
    chunk_size=500,
    n_drifts=2,
    concept_sigmoid_spacing=5,
    recurring=True
)

producer = KafkaProducer(bootstrap_servers='10.0.0.12:9092')
for k in range(n_chunks):
    producer.send('topic', b'k')

#poniżej wyświetlenie przykładowych chunków strumienia


cm = LinearSegmentedColormap.from_list(
    "lokomotiv", colors=[(0.3, 0.7, 0.3), (0.7, 0.3, 0.3)]
)

chunks_plotted = np.linspace(0, n_chunks - 1, 10).astype(int)


def plot_stream(data_str, filename="foo", title=""):
    fig, ax = plt.subplots(1, len(chunks_plotted), figsize=(14, 2.5))

    j = 0
    for i in range(n_chunks):
        X, y = data_str.get_chunk()
        if i in chunks_plotted:
            ax[j].set_title("Chunk %i" % i)
            ax[j].scatter(X[:, 0], X[:, 1], c=y, cmap=cm, s=10, alpha=0.5)
            ax[j].set_ylim(-4, 4)
            ax[j].set_xlim(-4, 4)
            ax[j].set(aspect="equal")
            j += 1

    fig.suptitle(title, fontsize=16)
    plt.tight_layout()
    plt.savefig("%s.png" % filename, transparent=False)


plot_stream(stream, "gradual", "Custom stream with recurring gradual drift")
