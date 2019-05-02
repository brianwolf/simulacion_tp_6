from administrador_tareas import Tarea,DificultadTarea
from enum import Enum

class PefilProgramador(Enum):
    Junior = "junior",
    Semisenior = "semisenior",
    Senior = "senior"

    def string_value(self,val):
        if type(val) is not str:
            return self.string_value(val[0])
        return val

    def name(self):
        return self.string_value(self.value)

class Administrador:
    def __init__(self, nro_programadores):
        self.programadores = nro_programadores
        self.programadores_ocupados=0
        self.tiempos_de_finalizacion=[]

    @property
    def programadores_disponibles(self):
        return self.programadores-self.programadores_ocupados

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        raise NotImplementedError("Administrador no esta implementando 'alguien_puede_resolver'")

    def tiempo_resolucion_tarea(self,tarea):
        raise NotImplementedError("Administrador no esta implementando 'tiempo_resolucion_tarea'")

    def poner_a_resolver_hasta(self,tiempo_finalizacion):
        self.programadores_ocupados+=1
        self.tiempos_de_finalizacion.append(tiempo_finalizacion)

    def finalizar_tarea(self,tarea:Tarea):
        self.programadores_ocupados-=1
        self.tiempos_de_finalizacion.remove(tarea.fecha_fin)
    

class AdministradorJuniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Junior
        return Administrador.__init__(self,nro_programadores)

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles>0 and tarea.tipo_tarea in [DificultadTarea.Simple,DificultadTarea.Complicada]
    
    
class AdministradorSemiseniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Semisenior
        return Administrador.__init__(self,nro_programadores)

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles>0 and tarea.tipo_tarea != DificultadTarea.Caotica


class AdministradorSeniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Senior 
        return Administrador.__init__(self,nro_programadores)
    
    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles>0

