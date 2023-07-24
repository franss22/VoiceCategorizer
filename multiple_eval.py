import subprocess

AMT = 1
RPT = 20

def run_test(amount:int):
    subprocess.run(["py", "create_test_data.py", "train", str(amount), "test_gen"])
    subprocess.run(["py", "voice_rec.py", "test_gen.wav", str(amount), "test_result.txt"])
    subprocess.run(["py", "eval.py", "test_result.txt", "test_gen.txt"])

def run_multiple(amount:int, repeat:int):
    for i in range(repeat):
        run_test(amount)

def avg(ls):
    return sum(ls)/len(ls)

def read_results():
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

    print(f"Average Precision: {avg(pre):.2f}")
    print(f"Average Recall: {avg(rec):.2f}")
    print(f"Average F1-Score: {avg(fsc):.2f}")


run_multiple(AMT, RPT)
read_results