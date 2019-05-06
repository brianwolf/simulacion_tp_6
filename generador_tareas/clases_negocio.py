from enum import Enum

class TipoTarea(Enum):
    FACIL='Simple'
    COMPLICADA='Complicada'
    COMPLEJA='Compleja'
    CAOTICA='Caotica'


class TipoPerfil(Enum):
    JUNIOR='junior'
    SEMISENIOR='semisenior'
    SENIOR='senior'


class Tarea():

    def __init__(self, tipo, perfil, fecha_crecion, fecha_inicio, fecha_fin):
        self.tipo = tipo
        self.perfil = perfil
        self.fecha_crecion = fecha_crecion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def dict(self):
        return {
            "tipo": str(self.tipo.value),
            "perfil": str(self.perfil.value),
            "fecha_crecion": str(self.fecha_crecion),
            "fecha_inicio": str(self.fecha_inicio),
            "fecha_fin": str(self.fecha_fin)
        }