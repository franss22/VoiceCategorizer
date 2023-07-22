import os
from pydub import AudioSegment
import sys
import random
from constants import *

# create_test_data [training_data_dir] [speaker_amount] [output_file]

if len(sys.argv) < 4:
    print(
        "Uso: {} [training_data_dir] [speaker_amount] [output_name]".format(sys.argv[0])
    )
    sys.exit(1)

training_data_dir = sys.argv[1]
if not os.path.isdir(training_data_dir):
    print("ERROR: no existe directorio {}".format(training_data_dir))
    sys.exit(1)

try:
    speaker_amount = int(sys.argv[2])
    if speaker_amount <1:
        print(f"ERROR: [speaker_amount]: {sys.argv[2]} must be a positive integer")
        sys.exit(1)
except:
    print(f"ERROR: [speaker_amount]: {sys.argv[2]} is not an int")
    sys.exit(1)


output_name = sys.argv[3]
if os.path.exists(output_name + ".wav"):
    print("Deleting old output_files {}".format(output_name))
    os.remove(output_name + ".wav")
    os.remove(output_name + ".txt")

speakers = os.listdir(training_data_dir)
chosen_speakers = random.choices(speakers, k=speaker_amount)

speakers_and_audios = []
for sp in chosen_speakers:
    files_dir = os.path.join(training_data_dir, sp)
    files = os.listdir(files_dir)
    files = [os.path.join(files_dir, f) for f in files]
    files = random.choices(files, k=SEGMENTS_PER_SPEAKER)
    speakers_and_audios += [(sp, f) for f in files]



random.shuffle(speakers_and_audios)


def generateCompleteAudio(speaker_and_file_list:list[tuple[any, str]]):
    completeAudio = None
    with open(output_name + ".txt", "w") as txt:
        remainder = 0
        i = 0
        lines = []
        for speaker,filename in speaker_and_file_list:
            sound: AudioSegment = AudioSegment.from_wav(filename)
            if completeAudio is None:
                completeAudio = sound
            else:
                completeAudio = completeAudio.append(sound)

            duration_ms = len(sound)
            first_segment = WINDOW_TIME_MS-remainder
            full_segments = (duration_ms-first_segment)//WINDOW_TIME_MS
            last_segment = (duration_ms-first_segment)%WINDOW_TIME_MS
            
            segment_amt = full_segments+1 if last_segment>0 else full_segments
            

            lines.append(f"{i*WINDOW_TIME_MS+remainder}\t{(i+1)*WINDOW_TIME_MS}\t{speaker}\n")
            i+=1
            remainder = last_segment

            for w in range(segment_amt):
                lines.append(f"{i*WINDOW_TIME_MS}\t{(i+1)*WINDOW_TIME_MS}\t{speaker}\n")
                i+=1
            lines.append(f"{i*WINDOW_TIME_MS}\t{i*WINDOW_TIME_MS+last_segment}\t{speaker}\n")
        txt.writelines(lines)
    completeAudio.export(out_f=output_name+".wav", format="wav")


        
generateCompleteAudio(speakers_and_audios)
