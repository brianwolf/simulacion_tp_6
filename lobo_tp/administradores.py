from generico import TipoPerfil, TipoTarea, Tarea, fecha_a_tiempo_simulacion
from configuracion import cantidad_juniors, cantidad_semiseniors, cantidad_seniors

# ------------------------------------------
# CONFIGURACION
# ------------------------------------------
tareas_habilitadas_senior = [TipoTarea.CAOTICA, TipoTarea.COMPLEJA, TipoTarea.COMPLICADA, TipoTarea.FACIL]
tareas_habilitadas_semisenior = [TipoTarea.COMPLEJA, TipoTarea.COMPLICADA, TipoTarea.FACIL]
tareas_habilitadas_junior = [TipoTarea.COMPLICADA, TipoTarea.FACIL]


# ------------------------------------------
# CLASES
# ------------------------------------------
class Singleton():
    
    __instancia = None
    admins = []

    def __new__(cls):
        if Singleton.__instancia is None:
            Singleton.__instancia = object.__new__(cls)

            admin_seniors = Administrador(cantidad_seniors, TipoPerfil.SENIOR, tareas_habilitadas_senior)
            admin_semiseniors = Administrador(cantidad_semiseniors, TipoPerfil.SEMISENIOR, tareas_habilitadas_semisenior)
            admin_juniors = Administrador(cantidad_juniors, TipoPerfil.JUNIOR, tareas_habilitadas_semisenior)
            
            Singleton.__instancia.admins = [admin_seniors, admin_semiseniors, admin_juniors]

        return Singleton.__instancia



class Administrador():

    def __init__(self, cantidad_personas:int, perfil: TipoPerfil, tareas_que_pueden_resolver: list):
        self.cantidad_personas = cantidad_personas
        self.perfil = perfil
        self.tareas_que_pueden_resolver = tareas_que_pueden_resolver
        
        self.tareas_en_proceso = []
        self.personas_ocupadas = 0


    def alguien_puede_resolver(self, tarea: Tarea) -> bool:
        tiene_el_perfil_necesario = tarea.perfil == self.perfil 
        return self.alguien_esta_libre() and tiene_el_perfil_necesario
    

    def poner_a_resolver(self, tarea: Tarea):
        self.personas_ocupadas += 1
        self.tareas_en_proceso.append(tarea)


    def alguien_esta_libre(self) -> bool:
        return self.personas_ocupadas < self.cantidad_personas

    
    def hay_tareas_resueltas(self, tiempo_simulacion: int):
        return any(fecha_a_tiempo_simulacion(tarea.fecha_fin) <= tiempo_simulacion for tarea in self.tareas_en_proceso)


    def resolver_salidas(self, tiempo_simulacion: int) -> list:

        tareas_resueltas = list(filter(lambda tarea: fecha_a_tiempo_simulacion(tarea.fecha_fin) <= tiempo_simulacion , self.tareas_en_proceso))
        self.personas_ocupadas -= len(tareas_resueltas)

        for tarea_resuelta in tareas_resueltas:
            self.tareas_en_proceso.remove(tarea_resuelta)

        return tareas_resueltas


# ------------------------------------------
# METODOS
# ------------------------------------------

def alguien_puede_resolver(tarea: Tarea) -> bool: 
    global Singleton
    return any(admin.alguien_puede_resolver(tarea) for admin in Singleton().admins)


def poner_a_resolver(tarea: Tarea):
    global Singleton
    admin_que_puede = next(admin for admin in Singleton().admins if admin.alguien_puede_resolver(tarea))
    admin_que_puede.poner_a_resolver(tarea)


def alguien_esta_libre():
    global Singleton
    return any(admin.alguien_esta_libre() for admin in Singleton().admins)


def hay_salidas(tiempo_simulacion: int) -> bool:
    global Singleton
    return any(admin.hay_tareas_resueltas(tiempo_simulacion) for admin in Singleton().admins) 


def resolver_salidas(tiempo_simulacion: int) -> list:
    global Singleton

    tareas_resueltas = []
    for resueltas in [admin.resolver_salidas(tiempo_simulacion) for admin in Singleton().admins]:
        tareas_resueltas.extend(resueltas)

    return tareas_resueltas


