import sys

if len(sys.argv) < 2:
    print("Uso: {} [predicted_data_txt] ".format(sys.argv[0]))
    sys.exit(1)

predicted_data_txt = sys.argv[1]


resultados = []
with open(predicted_data_txt) as source:
    for line in source:
        line = line.replace('\n','')
        fields = line.split('\t')
        resultados.append(fields)

print(resultados)