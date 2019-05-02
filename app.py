import configuracion
import funciones_datos
import generador_tareas
from administradores import AdministradorJuniors,AdministradorSemiseniors,AdministradorSeniors
from enum import Enum

class EventoTarea(Enum):
  llegada : "Llegada",
  salida : "Salida"

# --------------------------------------
# VARIABLES DE CONTROL
# ------------------------------------

tiempo_fin_simulacion = configuracion.obtener_tiempo_fin_simulacion()

administrador_juniors = AdministradorJuniors( configuracion.obtener_juniors() )
administrador_semiseniors = AdministradorSemiseniors( configuracion.obtener_semiseniors() )
administrador_seniors = AdministradorSeniors( configuracion.obtener_seniors() )

lista_administradores = [administrador_juniors, administrador_semiseniors, administrador_seniors]

# --------------------------------------
# VARIABLES DE ESTADO
# --------------------------------------
tiempo_sistema = 0 
lista_tareas = []

tiempo_juniors = 0
tiempo_semiseniors = 0
tiempo_seniors = 0


def incrementar_tiempo_sistema(lista_administradores,tiempo_sistema):
  return tiempo_sistema + 1


def resolver_tarea(tarea,tiempo_sistema):

	if any( administrador : administrador.alguien_puede_resolver( tarea ) for administrador in lista_administradores ):
	
    	administrador = next(administrador for administrador in lista_administradores if administrador.alguien_puede_resolver( tarea ) )
      
      	tiempo_finalizacion = tiempo_sistema + administrador.tiempo_resolucion_tarea( tarea )
        
		administrador.poner_a_resolver_hasta( tiempo_finalizacion )

        
def finalizar_tarea( tarea_finalizada, lista_administradores, tiempo_sistema ):
	
    lista_tareas.remove( tarea_finalizada )
    
    administrador = next(administrador for administrador in lista_administradores if administrador.tenes_esta_tarea( tarea_finalizada ) )
    administrador.finalizar_tarea( tarea_finalizada )
  
# -------------------------------------- 
# SIMULACION
# --------------------------------------

while tiempo_sistema < tiempo_fin_simulacion:
  
  	tarea_nueva = generador_tareas.generar_tarea_aleatoria()
    lista_tareas.append( tarea_nueva )
  
  	if hay_una_llegada( lista_tareas, tiempo_sistema):
        
        tarea_a_resolver = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.llegada)
        resolver_tarea( tarea_a_resolver )
        
    elif hay_una_salida(tiempo_sistema):
      tarea_a_finalizar = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.salida)
      finalizar_tarea(tarea_a_finalizar,lista_administradores,tiempo_sistema)
        
	tiempo_sistema = incrementar_tiempo_sistema(lista_administradores,tiempo_sistema)
    
metricas = calcular_resultados()

print(metricas)




    
    
    
    
    
    
    
    
    
    
    
    
