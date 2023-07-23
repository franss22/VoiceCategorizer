import sys
import os
import librosa as lbr
import scipy as sp
from sklearn.cluster import KMeans
import numpy as np
import random
from constants import *

def generate_features(audio,sr):
    '''
    Genera las features de cada window y las guarda en una lista de vectores
    '''
    samples_por_ventana = int(WINDOW_TIME_MS*sr/1000)
    print(samples_por_ventana)
    samples_salto = samples_por_ventana
    dimension = 64

    #samples, sr = lbr.load(archivo_wav)

    mfcc = lbr.feature.mfcc(y=audio, sr=sr, n_mfcc=dimension, n_fft=samples_por_ventana, hop_length=samples_salto)

    descriptores = mfcc.transpose()

    #TODO
    # Creo que ahora debiese normalizar los samples por ventana antes de pasar los descriptores

    #data = []
    #data.append([mfcc])
    #for i in range(500):
    #    data.append([random.randrange(0, 100)])
    return np.array(descriptores)

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

audio, sr = lbr.load(audio_path) #(0, 0)
print("Calculating descriptors...")
descriptors = generate_features(audio,sr)

print(f"Shape de descriptors es: {descriptors.shape}")


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
