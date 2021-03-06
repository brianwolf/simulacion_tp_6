import random
import configuracion

import uuid
from enum import Enum
from datetime import datetime

# ----------------------------------------------------
# ENUMS
# ----------------------------------------------------
class TipoTarea(Enum):
    SIMPLE = 'Simple'
    COMPLICADA = 'Complicada'
    COMPLEJA = 'Compleja'
    CAOTICA = 'Caotica'


class TipoPerfil(Enum):
    JUNIOR = 'junior'
    SEMISENIOR = 'semisenior'
    SENIOR = 'senior'


# ----------------------------------------------------
# CLASES
# ----------------------------------------------------
class Tarea():
    def __init__(self, tipo, perfil, fecha_crecion, fecha_inicio, fecha_fin, id=uuid.uuid4()):
        self.tipo = tipo
        self.perfil = perfil
        self.fecha_crecion = fecha_crecion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.id = id

    def dict(self):
        return {
            "tipo": str(self.tipo.value),
            "perfil": str(self.perfil.value),
            "fecha_crecion": str(self.fecha_crecion),
            "fecha_inicio": str(self.fecha_inicio),
            "fecha_fin": str(self.fecha_fin),
            "id": str(self.id)
        }

    def __eq__(self, value):
        return self.id == value.id


class TiempoProbabilidad():
    def __init__(self, tiempo, probabilidad):
        self.tiempo = tiempo
        self.probabilidad = probabilidad

    def dict(self):
        return self.__dict__()



# ----------------------------------------------------
# METODOS
# ----------------------------------------------------
def probabilidad_tiempo_random(lista_probabilidades: list) -> TiempoProbabilidad:
    
    numero_aleatorio = random.random()
    i = 0
    while i < len(lista_probabilidades):

        prob_anterior = 0 if i == 0 else prob_anterior + lista_probabilidades[i-1].probabilidad
        prob_siguiente = prob_anterior + lista_probabilidades[i].probabilidad

        if prob_anterior <= numero_aleatorio <= prob_siguiente:
            return lista_probabilidades[i]
        
        i+=1


def fecha_a_tiempo_simulacion(fecha: datetime) -> int:
    
    # tiempo_base = configuracion.fecha_inicial_tareas.timestamp()
    # tiempo_entrada = fecha.timestamp()

    # return tiempo_entrada - tiempo_base

    diferencia = fecha - configuracion.fecha_inicial_tareas
    return diferencia.seconds % 3600