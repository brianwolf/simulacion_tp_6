import configuracion
import generador_tareas
from generador_tareas import Tarea,agregar_nueva_tarea,actualizar_estado_tarea
from administradores import AdministradorJuniors, AdministradorSemiseniors, AdministradorSeniors
from enum import Enum


class EventoTarea(Enum):
  llegada = "Llegada",
  salida = "Salida"

# --------------------------------------
# VARIABLES DE CONTROL
# ------------------------------------


tiempo_fin_simulacion = configuracion.obtener_tiempo_fin_simulacion()

administrador_juniors = AdministradorJuniors(configuracion.obtener_juniors())
administrador_semiseniors = AdministradorSemiseniors(configuracion.obtener_semiseniors())
administrador_seniors = AdministradorSeniors(configuracion.obtener_seniors())

lista_administradores = [administrador_juniors, administrador_semiseniors, administrador_seniors]

# --------------------------------------
# VARIABLES DE ESTADO
# --------------------------------------
tiempo_sistema = 0
lista_tareas = []

tiempo_juniors = 0
tiempo_semiseniors = 0
tiempo_seniors = 0


def incrementar_tiempo_sistema(lista_administradores, tiempo_sistema):
  return tiempo_sistema + 1


def resolver_tarea(tarea, tiempo_sistema):

  administrador = next(administrador for administrador in lista_administradores if administrador.alguien_puede_resolver(tarea))

  if not administrador:
    return False

  tiempo_finalizacion = tiempo_sistema + administrador.tiempo_resolucion_tarea(tarea)

  administrador.poner_a_resolver_hasta(tiempo_finalizacion)

  actualizar_estado_tarea(lista_tareas,tarea,fecha_inicio=tiempo_sistema,fecha_fin=tiempo_finalizacion,perfil=administrador.perfil)

def finalizar_tarea(tarea_finalizada, lista_administradores, tiempo_sistema):

    lista_tareas.remove(tarea_finalizada)

    administrador = next(administrador for administrador in lista_administradores if administrador.tenes_esta_tarea(tarea_finalizada))
    administrador.finalizar_tarea(tarea_finalizada)

def hay_una_llegada( lista_tareas, tiempo_sistema)->bool:
    return any(tarea.fecha_inicio==tiempo_sistema for tarea in lista_tareas)

def hay_una_salida( lista_tareas, tiempo_sistema)->bool:
  return any(tarea.fecha_fin==tiempo_sistema for tarea in lista_tareas)

def obtener_tarea( lista_tareas, tiempo_sistema ,evento:EventoTarea)->Tarea:
  
  return next(tarea for tarea in lista_tareas if (evento==EventoTarea.llegada and tarea.fecha_inicio==tiempo_sistema) or
                                                  (evento==EventoTarea.salida and tarea.fecha_fin==tiempo_sistema))

def calcular_resultados():
  return {}

# --------------------------------------
# SIMULACION
# --------------------------------------


while tiempo_sistema < tiempo_fin_simulacion:

  lista_tareas = agregar_nueva_tarea(lista_tareas,tiempo_sistema)

  if hay_una_llegada( lista_tareas, tiempo_sistema):
      
      tarea_a_resolver = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.llegada)
      resolver_tarea( tarea_a_resolver )
      
  elif hay_una_salida(lista_tareas,tiempo_sistema):
    tarea_a_finalizar = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.salida)
    finalizar_tarea(tarea_a_finalizar,lista_administradores,tiempo_sistema)
      
  tiempo_sistema = incrementar_tiempo_sistema(lista_administradores,tiempo_sistema)
    
metricas = calcular_resultados()

print(metricas)




    
    
    
    
    
    
    
    
    
    
    
    
