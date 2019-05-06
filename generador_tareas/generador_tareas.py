import random
from datetime import datetime, timedelta

from clases_negocio import TipoPerfil, TipoTarea, Tarea


# ----------------------------------------------------
# CLASES
# ----------------------------------------------------

class TareaConfig():

    def __init__(self, tipo, perfil, probabilidad, fecha_inicio, fecha_final, duracion_minima_minutos, duracion_maxima_minutos):
        self.tipo = tipo
        self.perfil = perfil
        self.probabilidad = probabilidad
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.duracion_minima_minutos = duracion_minima_minutos
        self.duracion_maxima_minutos = duracion_maxima_minutos


# ----------------------------------------------------
# CONFIGURACION DE PROBABILIDADES
# ----------------------------------------------------
lista_tareas_config = [

        TareaConfig(TipoTarea.FACIL, TipoPerfil.JUNIOR, 0.25, datetime(2018,1,1), datetime(2018,6,30), 240, 1440),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SEMISENIOR, 0.14, datetime(2018,1,1), datetime(2018,6,30), 120, 480),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SENIOR, 0.01, datetime(2018,1,1), datetime(2018,6,30), 60, 120),

        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.JUNIOR, 0.10, datetime(2018,1,1), datetime(2018,6,30), 360, 2400),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SEMISENIOR, 0.20, datetime(2018,1,1), datetime(2018,6,30), 240, 960),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SENIOR, 0.05, datetime(2018,1,1), datetime(2018,6,30), 180, 480),

        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SEMISENIOR, 0.08, datetime(2018,1,1), datetime(2018,6,30), 480, 2400),
        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SENIOR, 0.12, datetime(2018,1,1), datetime(2018,6,30), 360, 1440),

        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SEMISENIOR, 0.01, datetime(2018,1,1), datetime(2018,6,30), 480, 1920),
        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SENIOR, 0.04, datetime(2018,1,1), datetime(2018,6,30), 480, 1440)
    ]


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------

def generar_fecha_random(fecha_desde: datetime, fecha_hasta: datetime) -> datetime:
    return fecha_desde + (fecha_hasta - fecha_desde) * random.random()


def generar_fechas_tarea(fecha_minima: datetime, fecha_maxima: datetime, duracion_minima, duracion_maxima):
   
    duracion = random.randint(duracion_minima, duracion_maxima)
    duracion_fecha = timedelta(0, duracion*60, 0)

    fecha_creacion = fecha_maxima
    fecha_inicio = fecha_maxima
    fecha_fin = fecha_minima

    while fecha_inicio >= fecha_fin + duracion_fecha:
        
        fecha_creacion = generar_fecha_random(fecha_minima, fecha_maxima)
        fecha_inicio = generar_fecha_random(fecha_creacion, fecha_maxima)
        fecha_fin = fecha_inicio + duracion_fecha

    return fecha_creacion, fecha_inicio, fecha_fin


def calcular_tarea_random() -> Tarea:

    prob_siguiente = 1.0
    prob_anterior = 0.0
    i = 0
    
    numero_aleatorio = random.random()
    
    while i < len(lista_tareas_config):

        prob_anterior = 0 if i == 0 else prob_anterior + lista_tareas_config[i-1].probabilidad
        prob_siguiente = prob_anterior + lista_tareas_config[i].probabilidad

        if prob_anterior <= numero_aleatorio <= prob_siguiente:
        
            tipo = lista_tareas_config[i].tipo
            perfil = lista_tareas_config[i].perfil

            duracion_maxima = lista_tareas_config[i].duracion_maxima_minutos
            duracion_minima = lista_tareas_config[i].duracion_minima_minutos
            fecha_maxima = lista_tareas_config[i].fecha_final
            fecha_minima = lista_tareas_config[i].fecha_inicio
            fecha_creacion, fecha_inicio, fecha_fin = generar_fechas_tarea(fecha_minima, fecha_maxima, duracion_minima, duracion_maxima)
            
            return Tarea(tipo, perfil, fecha_creacion, fecha_inicio, fecha_fin)
        
        i+=1
        
    print(f'Error en la logica: prob_anterior={prob_anterior}; numero_aleatorio={numero_aleatorio};  prob_siguiente={prob_siguiente}\n')


