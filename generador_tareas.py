import random
import json
import time

from generico import TipoTarea, TipoPerfil, ProbabilidadTiempo, Tarea, probabilidad_tiempo_random
from datetime import datetime, timedelta
from configuracion import get_config, UnidadTiempo

# ----------------------------------------------------
# CLASES
# ----------------------------------------------------

class TareaConfig():

    def __init__(self, tipo:TipoTarea, perfil:TipoPerfil, probabilidad:float, probabilidades:list):
        self.tipo = tipo
        self.perfil = perfil
        self.probabilidad = probabilidad
        self.probabilidades = probabilidades


# ----------------------------------------------------
# CONFIGURACION DE PROBABILIDADES
# ----------------------------------------------------

probabilidades_facil_junior = [
    ProbabilidadTiempo(4,0.1),
    ProbabilidadTiempo(8, 0.5),
    ProbabilidadTiempo(16,0.4),
]

probabilidades_facil_semisenior = [
    ProbabilidadTiempo(2, 0.5),
    ProbabilidadTiempo(4, 0.3),
    ProbabilidadTiempo(8, 0.2)
]

probabilidades_facil_senior = [
    ProbabilidadTiempo(1,0.9),
    ProbabilidadTiempo(2,0.1)
]

probabilidades_normal_junior = [
    ProbabilidadTiempo(4, 0.1),
    ProbabilidadTiempo(8, 0.2),
    ProbabilidadTiempo(16,0.3),
    ProbabilidadTiempo(24, 0.4),
]

probabilidades_normal_semisenior = [
    ProbabilidadTiempo(4, 0.5),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.2),
]

probabilidades_normal_senior = [
    ProbabilidadTiempo(2, 0.7),
    ProbabilidadTiempo(4, 0.3),
]

probabilidades_dificil_semisenior = [
    ProbabilidadTiempo(4, 0.5),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.2)
]

probabilidades_dificil_senior = [
    ProbabilidadTiempo(2, 0.3),
    ProbabilidadTiempo(4, 0.4),
    ProbabilidadTiempo(8, 0.3)
]

probabilidades_imposible_senior = [
    ProbabilidadTiempo(4, 0.5),
    ProbabilidadTiempo(8, 0.4),
    ProbabilidadTiempo(16, 0.1)
]

probabilidades_dias_tomar_tarea = [
    ProbabilidadTiempo(0, 0.4),
    ProbabilidadTiempo(1, 0.1),
    ProbabilidadTiempo(2, 0.1),
    ProbabilidadTiempo(3,0.2),
    ProbabilidadTiempo(4,0.1),
    ProbabilidadTiempo(5,0.1)
]


fecha_inicial_tareas = datetime(2018,1,1)
fecha_final_tareas = datetime(2019,4,30)

horario_laboral_inicial = 9
horario_laboral_salida = 18


lista_tareas_config = [

        TareaConfig(TipoTarea.FACIL, TipoPerfil.JUNIOR, 0.25, probabilidades_facil_junior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SEMISENIOR, 0.14, probabilidades_facil_semisenior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SENIOR, 0.01, probabilidades_facil_senior),

        TareaConfig(TipoTarea.NORMAL, TipoPerfil.JUNIOR, 0.10, probabilidades_normal_junior),
        TareaConfig(TipoTarea.NORMAL, TipoPerfil.SEMISENIOR, 0.20, probabilidades_normal_semisenior),
        TareaConfig(TipoTarea.NORMAL, TipoPerfil.SENIOR, 0.05, probabilidades_normal_senior),

        TareaConfig(TipoTarea.DIFICIL, TipoPerfil.SEMISENIOR, 0.08, probabilidades_dificil_semisenior),
        TareaConfig(TipoTarea.DIFICIL, TipoPerfil.SENIOR, 0.12, probabilidades_dificil_senior),
        
        TareaConfig(TipoTarea.IMPOSIBLE, TipoPerfil.SENIOR, 0.05, probabilidades_imposible_senior)
    ]


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------

def cambiar_a_hora_laboral(fecha: datetime) -> datetime:

    cumple_dia_laboral = fecha.strftime("%A") != "Saturday" and fecha.strftime("%A") != "Sunday"
    cumple_hora_laboral = horario_laboral_inicial <= fecha.hour <= horario_laboral_salida
    
    if not cumple_dia_laboral:
        if fecha.strftime("%A") == "Saturday":
            dias_a_sumar = 2
        if fecha.strftime("%A") == "Sunday":
            dias_a_sumar = 1
        return cambiar_a_hora_laboral(fecha + timedelta(days=dias_a_sumar))        

    if not cumple_hora_laboral:
        
        if fecha.hour < horario_laboral_inicial:
            fecha = fecha.replace(hour=24 - horario_laboral_salida + horario_laboral_inicial + fecha.hour)
            fecha += timedelta(days=1)

        if horario_laboral_salida < fecha.hour:
            fecha = fecha.replace(hour=horario_laboral_inicial + fecha.hour - horario_laboral_salida)
            fecha += timedelta(days=1)
        
        return cambiar_a_hora_laboral(fecha)

    return fecha


def generar_fecha_creacion() -> datetime:
    
    milisegundos = (fecha_final_tareas.timestamp() - fecha_inicial_tareas.timestamp()) * random.random()
    fecha_random = datetime.fromtimestamp(milisegundos + fecha_inicial_tareas.timestamp())
    
    return cambiar_a_hora_laboral(fecha_random)


def generar_fecha_que_se_toma(fecha_creacion: datetime) -> datetime:
    
    proba = probabilidad_tiempo_random(probabilidades_dias_tomar_tarea)
    fecha_random = fecha_creacion + timedelta(proba.tiempo,0,0)
    
    return cambiar_a_hora_laboral(fecha_random)


def generar_fechas_tarea(probabilidades_tiempo_resolucion:list):

    proba_resolucion = probabilidad_tiempo_random(probabilidades_tiempo_resolucion)
    duracion_fecha = timedelta(0, proba_resolucion.tiempo*3600, 0)

    fecha_creacion = fecha_final_tareas
    fecha_inicio = fecha_final_tareas
    fecha_fin = fecha_inicial_tareas

    while fecha_inicio >= fecha_fin + duracion_fecha:
        
        fecha_creacion = generar_fecha_creacion()
        fecha_inicio = generar_fecha_que_se_toma(fecha_creacion) + timedelta(0, horario_laboral_inicial, 0)
        fecha_fin = cambiar_a_hora_laboral(fecha_inicio + duracion_fecha)

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
            
            fecha_creacion, fecha_inicio, fecha_fin = generar_fechas_tarea(lista_tareas_config[i].probabilidades)
            
            return Tarea(tipo, perfil, fecha_creacion, fecha_inicio, fecha_fin)
        
        i+=1
        
    print(f'Error en la logica: prob_anterior={prob_anterior}; numero_aleatorio={numero_aleatorio};  prob_siguiente={prob_siguiente}\n')
    print(f'tipo={tipo};  perfil={perfil}\n')




# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------
if __name__ == "__main__":

    RUTA_JSON_SALIDA = './datos/tareas.json'
    TAREAS_A_GENERAR = 500

    lista_diccionarios = []
    while len(lista_diccionarios) < TAREAS_A_GENERAR:
        lista_diccionarios.append(crear_tarea_random().dict())

    archivo_salida = open(RUTA_JSON_SALIDA,"w+")
    archivo_salida.write(json.dumps(lista_diccionarios))