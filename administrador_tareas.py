from enum import Enum
from random import choice

class Tarea:
    def __init__(self, tarea_spec: dict):
        self.tipo_tarea = tarea_spec['tipo_tarea']
        self.perfil = tarea_spec['perfil']
        self.fecha_creacion = tarea_spec['fecha_creacion']
        self.fecha_inicio = tarea_spec['fecha_inicio']
        self.fecha_fin = tarea_spec['fecha_fin']

class DificultadTarea(Enum):
    Caotica = ("Caotico",0.7),
    Complicada = ("Complicado",0.37),
    Simple = ("Simple",0.25),
    Compleja = ("Complejo",0.31)

    def string_value(self,val):
        if type(val) is not str:
            return self.string_value(val[0])
        return val

    def name(self):
        return self.string_value(self.value)

def generar_tipo_tarea_aleatoria()->DificultadTarea:
    dificultades = [dificultad for dificultad in DificultadTarea]

    return choice(dificultades, 1,p=[d.value[1] for d in dificultades])

def generar_intervalo_de_arribo():
    return 1
    
def generar_fecha_creacion_aleatoria(tiempo_sistema):
    return tiempo_sistema+generar_intervalo_de_arribo()

def generar_tarea_aleatoria(tiempo_sistema):
    tarea_spec = {}
    tarea_spec['tipo_tarea'] = generar_tipo_tarea_aleatoria()
    tarea_spec['perfil'] = None
    tarea_spec['fecha_creacion'] = generar_fecha_creacion_aleatoria(tiempo_sistema)
    tarea_spec['fecha_inicio'] = None
    tarea_spec['fecha_fin'] = None
    
    return Tarea(tarea_spec)


def se_cumplio_intervalo_de_arribo(tiempo_sistema,lista_tareas) -> bool:
    if not lista_tareas:
        return False

    tarea:Tarea=lista_tareas.sort(key="fecha_creacion")[0]

    return tarea.fecha_creacion<=tiempo_sistema


def agregar_nueva_tarea(lista_tareas, tiempo_sistema):

    if not se_cumplio_intervalo_de_arribo(tiempo_sistema,lista_tareas):
        return lista_tareas

    tarea_nueva = generar_tarea_aleatoria(tiempo_sistema)
    lista_tareas.append(tarea_nueva)

    return lista_tareas

def actualizar_estado_tarea(lista_tareas,tarea:Tarea,fecha_inicio,fecha_fin,perfil):
    lista_tareas.remove(tarea)
    tarea.fecha_inicio=fecha_inicio
    tarea.fecha_fin=fecha_fin
    tarea.perfil = perfil

    lista_tareas.append(lista_tareas)

    return lista_tareas
    

