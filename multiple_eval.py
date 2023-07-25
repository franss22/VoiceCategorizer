import subprocess
import os

import sys

if len(sys.argv) < 3:
    print("Uso: {} [repeat] [speaker_amount] [successive=0]".format(sys.argv[0]))
    sys.exit(1)

repeat = int(sys.argv[1])
amount = int(sys.argv[2])
if len(sys.argv) >3:
    successive = int(sys.argv[3])
else:
    successive = 0
def run_test(amount:int):
    subprocess.check_output(["py", "create_test_data.py", "train", str(amount), "test_gen"])
    subprocess.check_output(["py", "voice_rec.py", "test_gen.wav", str(amount), "test_result.txt"])
    subprocess.check_output(["py", "eval.py", "test_result.txt", "test_gen.txt"])

def run_multiple(amount:int, repeat:int):
    for i in range(repeat):
        print(f"Running test {i} of {repeat}")
        run_test(amount)

def avg(ls):
    return sum(ls)/len(ls)

def read_results(amount):
    pre = []
    rec = []
    fsc = []
    with open("_eval.txt") as source:
        for line in source:
            line = line.replace('\n','')
            precision, recall, fscore = line.split('\t')
            precision, recall, fscore = (float(precision), float(recall), float(fscore))
            pre.append(precision)
            rec.append(recall)
            fsc.append(fscore)
    with open("_eval_mult.txt", "a") as f:
        f.write(f"{amount}\t{avg(pre):.2f}\t{avg(rec):.2f}\t{avg(fsc):.2f}\n")
    print(f"Average Precision: {avg(pre):.2f}")
    print(f"Average Recall: {avg(rec):.2f}")
    print(f"Average F1-Score: {avg(fsc):.2f}")

if successive == 0:
    os.remove("_eval.txt")
    run_multiple(amount, repeat)
    read_results(amount)
else:
    for i in range(amount):
        amt = i+1
        os.remove("_eval.txt")
        run_multiple(amt, repeat)
        read_results(amt)
