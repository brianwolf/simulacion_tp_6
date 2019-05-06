import random
import json

import generico
from generico import TipoTarea, TipoPerfil, ProbabilidadTiempo, Tarea
from datetime import datetime, timedelta


# ----------------------------------------------------
# CLASES
# ----------------------------------------------------

class TareaConfig():

    def __init__(self, tipo:TipoTarea, perfil:TipoPerfil, probabilidad:float, fecha_inicio:datetime, fecha_final:datetime, probabilidades:list):
        self.tipo = tipo
        self.perfil = perfil
        self.probabilidad = probabilidad
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.probabilidades = probabilidades


# ----------------------------------------------------
# CONFIGURACION DE PROBABILIDADES
# ----------------------------------------------------

probabilidades_facil_junior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_facil_semisenior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_facil_senior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complicado_junior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complicado_semisenior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complicado_senior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complejo_semisenior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complejo_senior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_caotico_semisenior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_caotico_senior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]


lista_tareas_config = [

        TareaConfig(TipoTarea.FACIL, TipoPerfil.JUNIOR, 0.25, datetime(2018,1,1), datetime(2018,6,30), probabilidades_facil_junior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SEMISENIOR, 0.14, datetime(2018,1,1), datetime(2018,6,30), probabilidades_facil_semisenior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SENIOR, 0.01, datetime(2018,1,1), datetime(2018,6,30), probabilidades_facil_senior),

        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.JUNIOR, 0.10, datetime(2018,1,1), datetime(2018,6,30), probabilidades_complicado_junior),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SEMISENIOR, 0.20, datetime(2018,1,1), datetime(2018,6,30), probabilidades_complicado_semisenior),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SENIOR, 0.05, datetime(2018,1,1), datetime(2018,6,30), probabilidades_complicado_senior),

        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SEMISENIOR, 0.08, datetime(2018,1,1), datetime(2018,6,30), probabilidades_complejo_semisenior),
        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SENIOR, 0.12, datetime(2018,1,1), datetime(2018,6,30), probabilidades_complejo_senior),

        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SEMISENIOR, 0.01, datetime(2018,1,1), datetime(2018,6,30), probabilidades_caotico_semisenior),
        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SENIOR, 0.04, datetime(2018,1,1), datetime(2018,6,30), probabilidades_caotico_senior)
    ]


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------

def generar_fecha_random(fecha_desde: datetime, fecha_hasta: datetime) -> datetime:
    return fecha_desde + (fecha_hasta - fecha_desde) * random.random()


def generar_fechas_tarea(fecha_minima: datetime, fecha_maxima: datetime, probabilidades_tiempo_resolucion:list):

    proba_resolucion = generico.probabilidad_tiempo_random(probabilidades_tiempo_resolucion)
    duracion_fecha = timedelta(0, proba_resolucion.tiempo*60, 0)

    fecha_creacion = fecha_maxima
    fecha_inicio = fecha_maxima
    fecha_fin = fecha_minima

    while fecha_inicio >= fecha_fin + duracion_fecha:
        
        fecha_creacion = generar_fecha_random(fecha_minima, fecha_maxima)
        fecha_inicio = generar_fecha_random(fecha_creacion, fecha_maxima)
        fecha_fin = fecha_inicio + duracion_fecha

    return fecha_creacion, fecha_inicio, fecha_fin

def crear_tarea_random() -> Tarea:

    i = 0
    numero_aleatorio = random.random()
    
    while i < len(lista_tareas_config):

        prob_anterior = 0 if i == 0 else prob_anterior + lista_tareas_config[i-1].probabilidad
        prob_siguiente = prob_anterior + lista_tareas_config[i].probabilidad

        if prob_anterior <= numero_aleatorio <= prob_siguiente:
        
            tipo = lista_tareas_config[i].tipo
            perfil = lista_tareas_config[i].perfil

            fecha_maxima = lista_tareas_config[i].fecha_final
            fecha_minima = lista_tareas_config[i].fecha_inicio
            fecha_creacion, fecha_inicio, fecha_fin = generar_fechas_tarea(fecha_minima, fecha_maxima, lista_tareas_config[i].probabilidades)
            
            return Tarea(tipo, perfil, fecha_creacion, fecha_inicio, fecha_fin)
        
        i+=1
        
    print(f'Error en la logica: prob_anterior={prob_anterior}; numero_aleatorio={numero_aleatorio};  prob_siguiente={prob_siguiente}\n')



# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------
if __name__ == "__main__":

    RUTA_JSON_SALIDA = './tareas.json'
    TAREAS_A_GENERAR = 10

    lista_tareas = []
    while len(lista_tareas) < TAREAS_A_GENERAR:
        lista_tareas.append(crear_tarea_random().dict())

    archivo_salida = open(RUTA_JSON_SALIDA,"w+")
    archivo_salida.write(str(json.dumps(lista_tareas)))