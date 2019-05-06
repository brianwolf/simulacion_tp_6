from administrador_tareas import Tarea,DificultadTarea
from enum import Enum
from numpy.random import choice
from configuracion import tiempos_de_resolucion_probables_de

class PefilProgramador(Enum):
    Junior = "junior"
    Semisenior = "semisenior"
    Senior = "senior"

class Administrador:
    def __init__(self, nro_programadores):
        self.programadores = nro_programadores
        self.programadores_ocupados=0
        self.tareas_en_progreso=[]

    def programadores_disponibles(self):
        return self.programadores-self.programadores_ocupados

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        raise NotImplementedError("Administrador no esta implementando 'alguien_puede_resolver'")

    def tiempo_resolucion_tarea(self,tarea):
        tiempos_de_resolucion = self.tiempos_de_resolucion_probables()
        return choice([tdr[0] for tdr in tiempos_de_resolucion], size=1,p=[tdr[1] for tdr in tiempos_de_resolucion],replace=True)[0]

    def tiempos_de_resolucion_probables(self):
        return tiempos_de_resolucion_probables_de(self.perfil.value)

    def poner_a_resolver_tarea(self,tarea):
        self.programadores_ocupados+=1
        self.tareas_en_progreso.append(tarea)

    def tenes_esta_tarea(self,tarea):
        return tarea in self.tareas_en_progreso

    def finalizar_tarea(self,tarea:Tarea):
        self.programadores_ocupados-=1
        self.tareas_en_progreso.remove(tarea)
    

class AdministradorJuniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Junior
        return Administrador.__init__(self,nro_programadores)

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles()>0 and tarea.tipo_tarea in [DificultadTarea.Simple,DificultadTarea.Complicada]

class AdministradorSemiseniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Semisenior
        return Administrador.__init__(self,nro_programadores)

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles()>0 and tarea.tipo_tarea != DificultadTarea.Caotica
    

class AdministradorSeniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Senior 
        return Administrador.__init__(self,nro_programadores)
    
    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles()>0
