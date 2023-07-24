import sys
import os
import librosa as lbd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.mixture import *
import pandas as pd
from constants import *

def VoiceActivityDetection(wavData):
    # uses the librosa library to compute short-term energy
    ste = lbd.feature.rms(y=wavData,hop_length=int(SR/FRAMERATE)).T
    thresh = 0.1*(np.percentile(ste,97.5) + 9*np.percentile(ste,2.5))    # Trim 5% off and set threshold as 0.1x of the ste range
    return (ste>thresh).astype('bool')

def trainGMM(wavData, vad2):
    global mfcc
    global vad
    mfcc = lbd.feature.mfcc(y=wavData, sr=SR, n_mfcc=32,hop_length=int(SR/FRAMERATE)).T
    vad = np.reshape(vad2,(len(vad2),))
    if mfcc.shape[0] > vad.shape[0]:
        vad = np.hstack((vad,np.zeros(mfcc.shape[0] - vad.shape[0]).astype('bool'))).astype('bool')
    elif mfcc.shape[0] < vad.shape[0]:
        vad = vad[:mfcc.shape[0]]
    mfcc = mfcc[vad,:];
    print("Training GMM..")
    GMM = GaussianMixture(n_components=5,covariance_type='diag').fit(mfcc)
    var_floor = 1e-5
    segLikes = []
    segSize = FRAMERATE*SEGLEN
    for segI in range(int(np.ceil(float(mfcc.shape[0])/(FRAMERATE*SEGLEN)))):
        startI = segI*segSize
        endI = (segI+1)*segSize
        if endI > mfcc.shape[0]:
            endI = mfcc.shape[0]-1
        if endI==startI:    # Reached the end of file
            break
        seg = mfcc[startI:endI,:]
        compLikes = np.sum(GMM.predict_proba(seg),0)
        segLikes.append(compLikes/seg.shape[0])
    print("Training Done")

    return np.asarray(segLikes)

def SegmentFrame(clust, numFrames):
    frameClust = np.zeros(numFrames)
    for clustI in range(len(clust)-1):
        frameClust[clustI*SEGLEN*FRAMERATE:(clustI+1)*SEGLEN*FRAMERATE] = clust[clustI]*np.ones(SEGLEN*FRAMERATE)
    frameClust[(clustI+1)*SEGLEN*FRAMERATE:] = clust[clustI+1]*np.ones(numFrames-(clustI+1)*SEGLEN*FRAMERATE)
    return frameClust

def speakerdiarisationdf(hyp, wavFile):
    
    starttime=[]
    endtime=[]
    speakerlabel=[]
            
    spkrChangePoints = np.where(hyp[:-1] != hyp[1:])[0]
    if spkrChangePoints[0]!=0 and hyp[0]!=-1:
        spkrChangePoints = np.concatenate(([0],spkrChangePoints))
    spkrLabels = []    
    for spkrHomoSegI in range(len(spkrChangePoints)):
        spkrLabels.append(hyp[spkrChangePoints[spkrHomoSegI]+1])
    for spkrI,spkr in enumerate(spkrLabels[:-1]):
        if spkr!=-1:
            #audioname.append(wavFile.split('/')[-1].split('.')[0]+".wav")
            starttime.append((spkrChangePoints[spkrI]+1)/float(FRAMERATE))
            endtime.append((spkrChangePoints[spkrI+1]-spkrChangePoints[spkrI])/float(FRAMERATE))
            speakerlabel.append("Speaker "+str(int(spkr)))
    if spkrLabels[-1]!=-1:
        #audioname.append(wavFile.split('/')[-1].split('.')[0]+".wav")
        starttime.append(spkrChangePoints[-1]/float(FRAMERATE))
        endtime.append((len(hyp) - spkrChangePoints[-1])/float(FRAMERATE))
        speakerlabel.append("Speaker "+str(int(spkrLabels[-1])))
    #
    speakerdf=pd.DataFrame({"starttime":starttime,"endtime":endtime,"speakerlabel":speakerlabel})
    
    spdatafinal=pd.DataFrame(columns=['SpeakerLabel','StartTime','EndTime'])
    i=0
    k=0
    spfind=""
    stime=""
    etime=""
    for row in speakerdf.itertuples():
        if(i==0):
            spfind=row.speakerlabel
            stime=row.starttime
        else:
            if(spfind==row.speakerlabel):
                etime=row.starttime        
            else:
                spdatafinal.loc[k]=[spfind,stime,row.starttime]
                k=k+1
                spfind=row.speakerlabel
                stime=row.starttime
        i=i+1
    spdatafinal.loc[k]=[spfind,stime,etime]
    return spdatafinal

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

wavData,SR = lbd.load(audio_path)

vad=VoiceActivityDetection(wavData)
mfcc = []

clusterset = trainGMM(wavData, vad)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(clusterset)  
# Normalizing the data so that the data approximately 
# follows a Gaussian distribution
X_normalized = normalize(X_scaled)

cluster = AgglomerativeClustering(n_clusters=expected_speaker_amount, affinity='euclidean', linkage='ward') 
clust=cluster.fit_predict(X_normalized)

frameClust = SegmentFrame(clust, mfcc.shape[0])

pass1hyp = -1*np.ones(len(vad))
pass1hyp[vad] = frameClust
spkdf=speakerdiarisationdf(pass1hyp, audio_path)
spkdf["TimeSeconds"]=spkdf.EndTime-spkdf.StartTime

if os.path.exists(output_file):
    print("Deleting old output_files {}".format(output_file))
    os.remove(output_file)


result_as_dict = spkdf.to_dict(orient='records')

results_txt = ""
for record in result_as_dict:
    results_txt += record['SpeakerLabel'] + "\t" + str(record['StartTime']) + "\t" + str(record['EndTime']) + "\t" + str(record['TimeSeconds']) + "\n"


with open(output_file, 'a') as f:
    f.write(results_txt)
