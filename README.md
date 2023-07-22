# VoiceCategorizer

Este proyecto consiste de un categorizador de voces, que dado un audio con múltiples personas hablando, categoriza los intervalos de tiempo del audio según qué voz está sonando.

## Utilización
Para utilizar el progranma, se debe llamar al script tal que:
```py categorize_speakers [audio_file] [speaker_amount] [output_file]```
Los argumentos son:
- **audio_file:** El path al archivo de audio que se desea procesar. El archivo debe estar en format `.wav`
- **speaker_amount:** La cantidad de voces distintas que tiene el audio.
- **output_file:** El path al archivo que se desea obtener.

### Ejemplo
Al correr el programa con 3 voces, entrega un resultado tal que así:
```
0  500  1
500  1000	2
1000	2500	1
2500	4500	2
4500	5000	1
5000	5500	2
5500	6000	0
6000	6500	2
6500	7000	0
7000	7500	2
7500	8000	0
8000	8500	2
```

Que indica que desde el milisegundo 0 al milisegundo 500 habla la voz 1, desde 500 a 100 la voz 2, desde 100 a 350 la voz 1, etc.

## Testing
Para testear y ajustar el programa se utiliza el dataset [Speaker Recognition - CMU ARCTIC](https://www.kaggle.com/datasets/mrgabrielblins/speaker-recognition-cmu-arctic) que consiste en una multitud de clips cortos de (de entre 1 a 5 segundos, aproximadamente), hablados por 18 personas distintas. 
Se utiliza `create_test_data.py` para generar audios mas largos, consistentes de multiples audios del dataset, concatenados al azar.
Este script funcoina tal que así:
`py create_test_data.py [training_data_dir] [speaker_amount] [output_file]`:
- **training_data_dir:** Debe ser una carpeta llena de subcarpetas. Cada cubcarpeta tiene un nombre distinto y representa una voz. Cada subcarpeta tiene dentro 1 o mas archivos de audio en formato `.wav` en donde habla unicamente la voz de la subcarpeta.
- **speaker_amount:** Indica la cantidad de voces distintas que se quiere que tenga el audio de testeo. 
- **output_file:** Indica el nombre (solo el nombre, sin la extensión de archivo) de los archivos de salida. El script crea los arvhivos `output_file.wav` con el audio creado y `output_file.txt` con el detalle de quien habla en qué momento.

Este script se puede utilizar con otros datasets, siempre que respeten la estructura esperada de training_data_dir y los audios estén en formato `.wav`.

