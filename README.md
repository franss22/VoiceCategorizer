# VoiceCategorizer

Este proyecto consiste de un categorizador de voces, que dado un audio con múltiples personas hablando, categoriza los intervalos de tiempo del audio según qué voz está sonando.

## Utilización
Para utilizar el progranma, se debe llamar al script tal que:
```py voice_rec.py [audio_file] [speaker_amount] [output_file]```
Los argumentos son:
- **audio_file:** El path al archivo de audio que se desea procesar. El archivo debe estar en format `.wav`
- **speaker_amount:** La cantidad de voces distintas que tiene el audio.
- **output_file:** El path al archivo que se desea obtener.

### Ejemplo
Al correr el programa con 2 voces, entrega un resultado tal que así:
```
Speaker 0	0.16	3.68	3.52
Speaker 1	3.68	11.42	7.74
Speaker 0	11.42	15.0	3.58
Speaker 1	15.0	22.42	7.42
Speaker 0	22.42	25.86	3.43
```

Que indica que desde el segundo 0.16 al 3.68 habla la voz 0 por 3.52 segundos, desde 3.68 al 11.42 la voz 1, etc.

## Creación de Audios para testing
Para testear y ajustar el programa se utiliza el dataset [Speaker Recognition - CMU ARCTIC](https://www.kaggle.com/datasets/mrgabrielblins/speaker-recognition-cmu-arctic) que consiste en una multitud de clips cortos de (de entre 1 a 5 segundos, aproximadamente), hablados por 18 personas distintas. 
Se utiliza `create_test_data.py` para generar audios mas largos, consistentes de multiples audios del dataset, concatenados al azar.
Este script se llama tal que:
`py create_test_data.py [training_data_dir] [speaker_amount] [output_file]`:
- **training_data_dir:** Debe ser una carpeta llena de subcarpetas. Cada cubcarpeta tiene un nombre distinto y representa una voz. Cada subcarpeta tiene dentro 1 o mas archivos de audio en formato `.wav` en donde habla unicamente la voz de la subcarpeta.
- **speaker_amount:** Indica la cantidad de voces distintas que se quiere que tenga el audio de testeo. 
- **output_file:** Indica el nombre (solo el nombre, sin la extensión de archivo) de los archivos de salida. El script crea los arvhivos `output_file.wav` con el audio creado y `output_file.txt` con el detalle de quien habla en qué momento.

Este script se puede utilizar con otros datasets, siempre que respeten la estructura esperada de training_data_dir y los audios estén en formato `.wav`.

## Evaluación
Para evaluar los resultados del sistema hay 2 scripts:
### Eval
`eval.py` calcula las estadisticas de precisión de 1 resultado. 
Este script se llama tal que:
`py eval.py [predicted_data_txt] [base_truth_txt]`:
- **predicted_data_txt:** es el archivo generado por `voice_rec`.
- **base_truth_txt:** es el archivo de texto generado por `create_test_data`.

Este script apende a `_eval.txt` la precisión, recall y F-score de la evaluación, en ese orden.

### Multiple_eval
`multiple_eval.py` evalúa los resultados multiples veces y los guarda en el archivo `_eval_mult.txt`. Los resultados guardados son Cantidad de hablantes, precisión, recall y F-score promedios de las evaluaciones, en ese orden
Este script se llama tal que:
`py mulitple_eval.py [repeat] [speaker_amount] [successive=0]`:
- **repeat:** Cuantas veces se repite la evaluación antes de promediarla y guardarla.
- **amount:** Cuantos hablantes tienen los audios generados.
- **successive:** Si este parametro es un entero que no sea 0, el script evaluará *repeat* veces para 0 hablantes, 1 hablante, ... hasta *amount* hablantes.