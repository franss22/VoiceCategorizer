import sys
from constants import *
from itertools import permutations
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
found_speakers = list(set([name for name, s, e, d in results]))
# print(results)

base_truth = []
with open(base_truth_txt, "r") as source:
    for line in source:
        line = line.replace('\n','')
        start, end, name = line.split('\t')
        base_truth.append([int(start), int(end), name])


base_speakers = list(set([name for s, e, name in base_truth]))
# print(base_truth)

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


windows = []

found_sp = None

for start, end, bsp in base_truth:
    found_sp, duration = find_speaker(start, end, results)
    if found_sp is None:
        windows.append((start, end, bsp, None))
        continue

    windows.append((start, end, bsp, found_sp))

print(windows)
print(base_speakers)
print(found_speakers)

speaker_amount = len(base_speakers)

def classify():
    '''
    Returns a dictionnary with each found speaker (speaker 1, speaker 2, etc), 
    with a dictionnary of how many times it was classified as each base speaker (axb, aup, etc)
    '''
    classification = {}
    for found_sp in found_speakers:
        classification[found_sp] = {}
        for base_sp in base_speakers:
            classification[found_sp][base_sp] = 0

    for start, end, expected_sp, found_sp in windows:
        if found_sp is None:
            continue
        classification[found_sp][expected_sp]+=1
    return classification

classification = classify()
print(classification)

err = {}
total_val = 0
for fsp in classification:
    err[fsp] = {}
    total = sum(classification[fsp].values())
    total_val += total
    for bsp in classification[fsp]:
        err[fsp][bsp] = total-classification[fsp][bsp]


# We assign each found speaker to a different base speaker, minimizing the error

min_err = len(base_truth)

alias = {}
for opt in permutations(base_speakers):
    opt_err = 0
    for i in range(speaker_amount):
        fsp = found_speakers[i]
        bsp = opt[i]
        opt_err += err[fsp][bsp]
    if opt_err < min_err:
        min_err = opt_err
        alias = {found_speakers[i]:opt[i] for i in range(speaker_amount)}







# print(windows)
good, bad, none = (0, 0, 0)
speaker_correctness = {}
for sp in base_speakers:
    
    speaker_correctness[sp]= {
        "tp":0,
        "fp":0,
        "fn":0
    }

def determine_correctness(expected, found, assign=alias):
    if found is None:
        return None
    else:
        return assign[found] == expected

for start, end, expected, found in windows:
    correct = determine_correctness(expected, found)
    if correct is None:
        speaker_correctness[expected]["fn"] +=1
        none +=1
        # bad+=1
    elif correct is True:
        speaker_correctness[expected]["tp"] +=1
        good +=1
    else:
        speaker_correctness[expected]["fn"] +=1
        speaker_correctness[expected]["fp"] +=1
        bad +=1
print(f"Correct identifications: {good}\nWrong identifications: {bad}\nUnknown: {none}")


total_recall = 0
total_precision = 0
total_fscore = 0
for bsp, stats in speaker_correctness.items():
    print(f"Speaker {bsp}, identified as {[k for k, v in alias.items() if v == bsp][0]}:")
    precision = stats["tp"]/(stats["tp"]+stats["fp"]+0.000001)
    total_precision+=precision
    recall = stats["tp"]/(stats["tp"]+stats["fn"]+0.000001)
    total_recall+=recall
    fscore = 2*(precision*recall)/(precision+recall+0.000001)
    total_fscore+=fscore
    print(f"- Precision: {precision*100:.2f}")
    print(f"- Recall: {recall*100:.2f}")
    print(f"- F1-Score: {fscore*100:.2f}")



avg_precision = total_precision/speaker_amount
avg_recall = total_recall/speaker_amount
avg_fscore = total_fscore/speaker_amount
print(f"Average Precision: {avg_precision:.2f}")
print(f"Average Recall: {avg_recall:.2f}")
print(f"Average F1-Score: {avg_fscore:.2f}")


with open("_eval.txt", "a") as f:
    f.write(f"{avg_precision}\t{avg_recall}\t{avg_fscore}\n")

