import generador_tareas
import json

RUTA_JSON_SALIDA = './tareas.json'
TAREAS_A_REALIZAR = 10000

# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------
lista_tareas = []
while len(lista_tareas) < TAREAS_A_REALIZAR:
    lista_tareas.append(generador_tareas.calcular_tarea_random().dict())

archivo_salida = open(RUTA_JSON_SALIDA,"w+")
archivo_salida.write(str(json.dumps(lista_tareas)))