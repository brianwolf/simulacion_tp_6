import random
from enum import Enum

# ----------------------------------------------------
# ENUMS
# ----------------------------------------------------
class TipoTarea(Enum):
    FACIL = 'facil'
    NORMAL = 'normal'
    DIFICIL = 'dificil'
    IMPOSIBLE = 'imposible'


class TipoPerfil(Enum):
    JUNIOR = 'junior'
    SEMISENIOR = 'semisenior'
    SENIOR = 'senior'


# ----------------------------------------------------
# CLASES
# ----------------------------------------------------
class Tarea():
    def __init__(self, tipo, perfil, fecha_creacion, fecha_inicio, fecha_fin):
        self.tipo = tipo
        self.perfil = perfil
        self.fecha_creacion = fecha_creacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def dict(self):
        return {
            "tipo": str(self.tipo.value),
            "perfil": str(self.perfil.value),
            "fecha_creacion": str(self.fecha_creacion),
            "fecha_inicio": str(self.fecha_inicio),
            "fecha_fin": str(self.fecha_fin)
        }


class ProbabilidadTiempo():
    def __init__(self, tiempo, probabilidad):
        self.tiempo = tiempo
        self.probabilidad = probabilidad

    def dict(self):
        return self.__dict__()



# ----------------------------------------------------
# METODOS
# ----------------------------------------------------
def probabilidad_tiempo_random(lista_probabilidades: list) -> ProbabilidadTiempo:
    
    numero_aleatorio = random.random()
    i = 0
    while i < len(lista_probabilidades):

        prob_anterior = 0 if i == 0 else prob_anterior + lista_probabilidades[i-1].probabilidad
        prob_siguiente = prob_anterior + lista_probabilidades[i].probabilidad

        if prob_anterior <= numero_aleatorio <= prob_siguiente:
            return lista_probabilidades[i]
        
        i+=1