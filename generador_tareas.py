import random
import json

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

probabilidades_simple_junior = [
    ProbabilidadTiempo(1, 0.1),
    ProbabilidadTiempo(2, 0.1),
    ProbabilidadTiempo(4,0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
]

probabilidades_simple_semisenior = [
    ProbabilidadTiempo(1, 0.2),
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3)
]

probabilidades_simple_senior = [
    ProbabilidadTiempo(2,0.7),
    ProbabilidadTiempo(4,0.3)
]

probabilidades_complicado_junior = [
    ProbabilidadTiempo(4, 0.1),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
    ProbabilidadTiempo(24, 0.2),
    ProbabilidadTiempo(32,0.1)
]

probabilidades_complicado_semisenior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
    ProbabilidadTiempo(24, 0.2)
]

probabilidades_complicado_senior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.5),
    ProbabilidadTiempo(16,0.3)
]

probabilidades_complejo_semisenior = [
    ProbabilidadTiempo(2, 0.05),
    ProbabilidadTiempo(4, 0.1),
    ProbabilidadTiempo(8, 0.1),
    ProbabilidadTiempo(16,0.2),
    ProbabilidadTiempo(32,0.3),
    ProbabilidadTiempo(48,0.25)
]

probabilidades_complejo_senior = [
    ProbabilidadTiempo(2, 0.2),
    ProbabilidadTiempo(4, 0.3),
    ProbabilidadTiempo(8, 0.2),
    ProbabilidadTiempo(16,0.2),
    ProbabilidadTiempo(32,0.1)
]

probabilidades_caotico_semisenior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16, 0.1),
    ProbabilidadTiempo(32,0.3),
    ProbabilidadTiempo(48,0.1)
]

probabilidades_caotico_senior = [
    ProbabilidadTiempo(4, 0.3),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16, 0.2),
    ProbabilidadTiempo(32,0.2)
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

        TareaConfig(TipoTarea.FACIL, TipoPerfil.JUNIOR, 0.25, probabilidades_simple_junior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SEMISENIOR, 0.14, probabilidades_simple_semisenior),
        TareaConfig(TipoTarea.FACIL, TipoPerfil.SENIOR, 0.01, probabilidades_simple_senior),

        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.JUNIOR, 0.10, probabilidades_complicado_junior),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SEMISENIOR, 0.20, probabilidades_complicado_semisenior),
        TareaConfig(TipoTarea.COMPLICADA, TipoPerfil.SENIOR, 0.05, probabilidades_complicado_senior),

        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SEMISENIOR, 0.08, probabilidades_complejo_semisenior),
        TareaConfig(TipoTarea.COMPLEJA, TipoPerfil.SENIOR, 0.12, probabilidades_complejo_senior),

        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SEMISENIOR, 0.01, probabilidades_caotico_semisenior),
        TareaConfig(TipoTarea.CAOTICA, TipoPerfil.SENIOR, 0.04, probabilidades_caotico_senior)
    ]


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------

def cambiar_a_hora_laboral(fecha: datetime) -> datetime:

    fecha_final = datetime(fecha.year, fecha.month, fecha.day, fecha.hour, fecha.minute, fecha.second, fecha.microsecond)
    
    while not (horario_laboral_inicial <= fecha_final.hour <= horario_laboral_salida):
        
        optativo = 24 if fecha_final.hour < horario_laboral_salida else 0
        hora_correcta = fecha_final.hour - horario_laboral_salida + horario_laboral_inicial + optativo

        fecha_final += timedelta(1,0,0)
        fecha_final = fecha_final.replace(hour=hora_correcta)
        
    return fecha_final


def generar_fecha_creacion(fecha_desde: datetime, fecha_hasta: datetime) -> datetime:
    fecha_random = datetime.utcnow()
    while fecha_random.hour > horario_laboral_salida or fecha_random.hour < horario_laboral_inicial:
        fecha_random = fecha_desde + (fecha_hasta - fecha_desde) * random.random()

    return cambiar_a_hora_laboral(fecha_random)


def generar_fecha_que_se_toma(fecha_creacion: datetime) -> datetime:
    
    proba = probabilidad_tiempo_random(probabilidades_dias_tomar_tarea)
    fecha_random = fecha_creacion + timedelta(proba.tiempo,0,0)
    
    return cambiar_a_hora_laboral(fecha_random)


def generar_fechas_tarea(fecha_minima: datetime, fecha_maxima: datetime, probabilidades_tiempo_resolucion:list):

    proba_resolucion = probabilidad_tiempo_random(probabilidades_tiempo_resolucion)
    duracion_fecha = timedelta(0, proba_resolucion.tiempo*3600, 0)

    fecha_creacion = fecha_maxima
    fecha_inicio = fecha_maxima
    fecha_fin = fecha_minima

    while fecha_inicio >= fecha_fin + duracion_fecha:
        
        fecha_creacion = generar_fecha_creacion(fecha_minima, fecha_maxima)
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

            # fecha_maxima = lista_tareas_config[i].fecha_final
            # fecha_minima = lista_tareas_config[i].fecha_inicio
            fecha_creacion, fecha_inicio, fecha_fin = generar_fechas_tarea(fecha_inicial_tareas, fecha_final_tareas, lista_tareas_config[i].probabilidades)
            
            return Tarea(tipo, perfil, fecha_creacion, fecha_inicio, fecha_fin)
        
        i+=1
        
    print(f'Error en la logica: prob_anterior={prob_anterior}; numero_aleatorio={numero_aleatorio};  prob_siguiente={prob_siguiente}\n')



# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------
if __name__ == "__main__":

    RUTA_JSON_SALIDA = './datos/tareas.json'
    TAREAS_A_GENERAR = 2000

    lista_tareas = []
    while len(lista_tareas) < TAREAS_A_GENERAR:
        lista_tareas.append(crear_tarea_random().dict())

    archivo_salida = open(RUTA_JSON_SALIDA,"w+")
    archivo_salida.write(str(json.dumps(lista_tareas)))