from administrador_tareas import Tarea,DificultadTarea
from enum import Enum

class PefilProgramador(Enum):
    Junior = "junior"
    Semisenior = "semisenior"
    Senior = "senior"

class Administrador:
    def __init__(self, nro_programadores):
        self.programadores = nro_programadores
        self.programadores_ocupados=0
        self.tiempos_de_finalizacion=[]

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
        return self.programadores_disponibles()>0 and tarea.tipo_tarea in [DificultadTarea.Simple,DificultadTarea.Complicada]

    def tiempo_resolucion_tarea(self,tarea:Tarea):
        return 10
    
    
class AdministradorSemiseniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Semisenior
        return Administrador.__init__(self,nro_programadores)

    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles()>0 and tarea.tipo_tarea != DificultadTarea.Caotica
    
    def tiempo_resolucion_tarea(self,tarea:Tarea):
        return 4


class AdministradorSeniors(Administrador):
    def __init__(self, nro_programadores):
        self.perfil = PefilProgramador.Senior 
        return Administrador.__init__(self,nro_programadores)
    
    def alguien_puede_resolver(self,tarea:Tarea)->bool:
        return self.programadores_disponibles()>0

    def tiempo_resolucion_tarea(self,tarea:Tarea):
        return 1

