import sys
import os
import librosa as lbr
import scipy as sp
from sklearn.cluster import KMeans
import numpy as np

WINDOW = 128 # Window time en ms

def generate_features(audio, sr):
    '''
    Genera las features de cada window y las guarda en una lista de vectores
    '''
    raise NotImplementedError()

if len(sys.argv) < 3:
    print("Uso: {} [archivo_audio] [cantidad_de_hablantes]".format(sys.argv[0]))
    sys.exit(1)

audio_path = sys.argv[1]
expected_speaker_amount = sys.argv[2]

if not os.path.isfile(audio_path):
    print(f"ERROR: {audio_path} is not a file")
    sys.exit(1)

if os.path.splitext(audio_path)[-1] != ".wav":
    print(f"ERROR: {audio_path} is not a .wav file")
    sys.exit(1)

audio, sr = lbr.load(audio_path)
descriptors = generate_features(audio, sr)

kmeans = KMeans(n_clusters=expected_speaker_amount).fit(descriptors)
# To Do: el resto del código xd