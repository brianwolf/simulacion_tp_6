from enum import Enum
from numpy.random import choice
from configuracion import probabilidad_tipo_tarea,intervalo_de_arribo
import datetime

def converter(o):
    if isinstance(o, datetime.datetime):
        return o.strftime("%d/%m/%yT%H:%M:%SZ")
    elif isinstance(o, datetime.date):
        return o.strftime("%d/%m/%y")
    else:
        return str(o) 


class Tarea:
    def __init__(self, tarea_spec: dict):
        self.tipo_tarea = tarea_spec['tipo_tarea']
        self.perfil = tarea_spec['perfil']
        self.fecha_creacion = tarea_spec['fecha_creacion']
        self.fecha_inicio = tarea_spec['fecha_inicio']
        self.fecha_fin = tarea_spec['fecha_fin']
    
    def get_dict(self):
        return {'tipo_tarea': None if self.tipo_tarea is None else self.tipo_tarea.value[0],
                'perfil': None if self.perfil is None else self.perfil.value,
                'fecha_creacion': converter(self.fecha_creacion),
                'fecha_inicio': converter(self.fecha_inicio),
                'fecha_fin': converter(self.fecha_fin)}

    def id(self):
        return self.tipo_tarea,self.fecha_creacion

    def __hash__(self):
        return hash(self.id())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.get_dict())

    def __eq__(self,other):
        return self.id()==other.id()

class DificultadTarea(Enum):
    Caotica = ("Caotico",probabilidad_tipo_tarea("Caotico"))
    Complicada = ("Complicado",probabilidad_tipo_tarea("Complicado"))
    Simple = ("Simple",probabilidad_tipo_tarea("Simple"))
    Compleja = ("Complejo",probabilidad_tipo_tarea("Complejo"))

def generar_tipo_tarea_aleatoria()->DificultadTarea:
    dificultades = [dificultad for dificultad in DificultadTarea]
    probabilidades = [d.value[1] for d in dificultades]

    return choice(dificultades, size=1,p=probabilidades,replace=True)[0]

def generar_intervalo_de_arribo():
    return 1
    
def generar_fecha_creacion_aleatoria(tiempo_sistema):
    return tiempo_sistema+intervalo_de_arribo(tiempo_sistema)

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
    fecha_creacion_minima=min(map(lambda t:t.fecha_creacion,lista_tareas))

    return fecha_creacion_minima<=tiempo_sistema


def agregar_nueva_tarea(lista_tareas, tiempo_sistema,primera_iteracion=False):

    if not primera_iteracion and not se_cumplio_intervalo_de_arribo(tiempo_sistema,lista_tareas):
        return lista_tareas

    tarea_nueva = generar_tarea_aleatoria(tiempo_sistema)
    lista_tareas.append(tarea_nueva)

    return lista_tareas

def actualizar_estado_tarea(lista_tareas,tarea:Tarea,fecha_inicio,fecha_fin,perfil):
    lista_tareas.remove(tarea)
    tarea.fecha_inicio=fecha_inicio
    tarea.fecha_fin=fecha_fin
    tarea.perfil = perfil

    lista_tareas.append(tarea)

    return lista_tareas
    

