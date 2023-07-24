import sys
from constants import *

if len(sys.argv) < 3:
    print("Uso: {} [predicted_data_txt] [base_truth_txt]".format(sys.argv[0]))
    sys.exit(1)

predicted_data_txt = sys.argv[1]
base_truth_txt = sys.argv[2]


results = []
with open(predicted_data_txt) as source:
    for line in source:
        line = line.replace('\n','')
        name, start, end, duration = line.split('\t')
        results.append([name, float(start), float(end), float(duration)])

print(results)

base_truth = []
with open(base_truth_txt, "r") as source:
    for line in source:
        line = line.replace('\n','')
        start, end, name = line.split('\t')
        base_truth.append([int(start), int(end), name])

# print(base_truth)

identified_speakers = {}
interval = 0
def find_speaker(start_ms, end_ms, res):
    start_s = start_ms/1000
    end_s = end_ms/1000
    for sp, start, end, duration in res:
        if start_s > end:
            continue
        if start_s >= start and end_s <end:
            return sp, duration*1000
        
    return None, None


correctness = []

sp = None
for start, end, speaker in base_truth:
    
    if interval == 0:
        sp, duration = find_speaker(start, end, results)
        if sp is None:
            correctness.append((start, end, None, identified_speakers.get(speaker, None), None))
            continue
        if sp is not None:
            interval = duration//WINDOW_TIME_MS+1
    interval-=1
    id_sp = identified_speakers.setdefault(speaker, sp)
    correctness.append((start, end, id_sp == sp, id_sp, sp))
with open("Eval_results.tsv", "w") as f:
    f.write("#start\tend\tcorrect\texpected_speaker\tfound_speaker\n")
    for line in correctness:
        l = [str(x) for x in line]
        f.write("\t".join(l)+"\n")

print(correctness)

    

