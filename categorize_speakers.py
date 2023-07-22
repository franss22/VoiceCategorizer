import sys
import os
import librosa as lbr
import scipy as sp
from sklearn.cluster import KMeans
import numpy as np
import random
from constants import *


def generate_features(audio, sr):
    '''
    Genera las features de cada window y las guarda en una lista de vectores
    '''
    data = []
    for i in range(500):
        data.append([random.randrange(0, 100)])
    return np.array(data)

    # raise NotImplementedError()

def get_speaker_windows(speaker, kmeans:KMeans):
    return np.where(kmeans.labels_==speaker)[0]


if len(sys.argv) < 4:
    print("Uso: {} [audio_file] [speaker_amount] [output_file]".format(sys.argv[0]))
    sys.exit(1)

audio_path = sys.argv[1]
try:
    expected_speaker_amount = int(sys.argv[2])
    if expected_speaker_amount <1:
        print(f"ERROR: [speaker_amount]: {sys.argv[2]} must be a positive integer")
        sys.exit(1)
except:
    print(f"ERROR: [speaker_amount]: {sys.argv[2]} is not an int")
output_file = sys.argv[3]

if not os.path.isfile(audio_path):
    print(f"ERROR: [audio_file]: {audio_path} is not a file")
    sys.exit(1)

if os.path.splitext(audio_path)[-1] != ".wav":
    print(f"ERROR: [audio_file]: {audio_path} is not a .wav file")
    sys.exit(1)

audio, sr = (0, 0)#lbr.load(audio_path)
print("Calculating descriptors...")
descriptors = generate_features(audio, sr)


print("Clustering data...")
kmeans = KMeans(n_clusters=expected_speaker_amount, n_init="auto").fit(descriptors)


print("Saving results...")
previous_speaker = kmeans.labels_[0]
w_i = 0
w_f = 0
with open(output_file, "w") as f:
    for index, speaking in enumerate(kmeans.labels_):
        if speaking != previous_speaker:
            w_f = index
            f.write(f"{w_i*WINDOW_TIME_MS}\t{w_f*WINDOW_TIME_MS}\t{previous_speaker}\n")
            w_i = index
            previous_speaker = speaking
        else:
            w_f = index
    f.write(f"{w_i*WINDOW_TIME_MS}\t{w_f*WINDOW_TIME_MS}\t{previous_speaker}")
print("Done!")
