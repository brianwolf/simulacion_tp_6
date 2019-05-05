import configuracion
import administrador_tareas
from administrador_tareas import Tarea,agregar_nueva_tarea,actualizar_estado_tarea,DificultadTarea
from administradores import AdministradorJuniors, AdministradorSemiseniors, AdministradorSeniors,PefilProgramador
from enum import Enum
from progress.bar import Bar


class EventoTarea(Enum):
  Llegada = "Llegada",
  Salida = "Salida"

class ResultadoSimulacion:
  def __init__(self,tiempo_finalizacion,administradores):
    self.historico_tareas=[]
    self.tiempos_de_ocio=[{"perfil":admin.perfil,"tiempo_ocioso":0,"cantidad_programadores":admin.programadores} for admin in administradores]
    self.tiempo_finalizacion = tiempo_finalizacion
  
  def agregar_tiempo_ocioso(self,perfil,cantidad_personas_al_pedo):
    mapa_de_ocio = next(mapa for mapa in self.tiempos_de_ocio if mapa["perfil"]==perfil)
    mapa_de_ocio.update({"tiempo_ocioso":mapa_de_ocio["tiempo_ocioso"]+cantidad_personas_al_pedo})

  def generar_metricas(self,lista_tareas):
    tiempos_de_resolucion_promedio = self.calcular_tiempos_resolucion_promedio()
    porcentajes_de_tiempos_de_ocio = self.calcular_porcentajes_de_tiempos_de_ocio()
    porcentaje_de_tareas_realizadas = self.calcular_porcentaje_de_tareas_realizadas(lista_tareas)

    print(f'TAREAS SIN HACER: {lista_tareas}\n')

    return {"PTR":porcentaje_de_tareas_realizadas,"TPR":tiempos_de_resolucion_promedio,"PTO":porcentajes_de_tiempos_de_ocio}

  def calcular_tiempos_resolucion_promedio(self):
    tiempos_promedio_por_dificultad = []

    # print(f'TAREAS HISTORICO: {self.historico_tareas}\n')
    # print(f'OCIO:{self.tiempos_de_ocio}\n')

    for dificultad in DificultadTarea:
      tareas_de_dificultad = list(filter(lambda t: t.tipo_tarea==dificultad,self.historico_tareas))
      print(f'TAREAS {dificultad.value[0]}: {tareas_de_dificultad}\n')
      cant_tareas = max(len(tareas_de_dificultad),1)
      promedio = sum(map(lambda t : t.fecha_fin-t.fecha_creacion ,tareas_de_dificultad))/cant_tareas
      
      #Fix para un json mas amigable, en vez de tener ('Caotico', 1.0) lo cambio por {"Caotico":1.0}
      #tiempos_promedio_por_dificultad.append((dificultad.value[0],promedio))
      tiempos_promedio_por_dificultad.append({dificultad.value[0]:promedio})

      
    return tiempos_promedio_por_dificultad

  def calcular_porcentajes_de_tiempos_de_ocio(self):
    return [{"perfil":e["perfil"].value,"porcentaje":e["tiempo_ocioso"]/(self.tiempo_finalizacion*e["cantidad_programadores"])} for e in self.tiempos_de_ocio]
  
  def calcular_porcentaje_de_tareas_realizadas(self,lista_tareas):
    H = len(historico_tareas)
    L = len(lista_tareas)
    total = max(1,H+L)
    return H/total

  

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

# --------------------------------------
# VARIABLES EXTRA
# --------------------------------------
historico_tareas = []
resultado_simulacion = ResultadoSimulacion(tiempo_fin_simulacion,lista_administradores)

def incrementar_tiempo_sistema(lista_administradores, tiempo_sistema):
  return tiempo_sistema + 1


def resolver_tarea(tarea, tiempo_sistema,lista_administradores):

  if not any(a.alguien_puede_resolver(tarea) for a in lista_administradores):
    return

  administrador = next(administrador for administrador in lista_administradores if administrador.alguien_puede_resolver(tarea))

  tiempo_finalizacion = tiempo_sistema + administrador.tiempo_resolucion_tarea(tarea)

  administrador.poner_a_resolver_tarea(tarea)

  actualizar_estado_tarea(lista_tareas,tarea,fecha_inicio=tiempo_sistema,fecha_fin=tiempo_finalizacion,perfil=administrador.perfil)

def finalizar_tarea(tarea_finalizada, lista_administradores, tiempo_sistema):

  historico_tareas.append(tarea_finalizada)
  lista_tareas.remove(tarea_finalizada)

  administrador = next(administrador for administrador in lista_administradores if administrador.tenes_esta_tarea(tarea_finalizada))
  administrador.finalizar_tarea(tarea_finalizada)

def hay_una_llegada( lista_tareas, tiempo_sistema)->bool:
    return any(tarea.fecha_creacion==tiempo_sistema for tarea in lista_tareas)

def hay_una_salida( lista_tareas, tiempo_sistema)->bool:
  return any(tarea.fecha_fin==tiempo_sistema for tarea in lista_tareas)

def obtener_tarea( lista_tareas, tiempo_sistema ,evento:EventoTarea)->Tarea:
  
  return next(tarea for tarea in lista_tareas if (evento==EventoTarea.Llegada and tarea.fecha_creacion==tiempo_sistema) or
                                                  (evento==EventoTarea.Salida and tarea.fecha_fin==tiempo_sistema))

def actualizar_tiempos_ociosos():
  for admin in lista_administradores:
    resultado_simulacion.agregar_tiempo_ocioso(admin.perfil,admin.programadores_disponibles())

# --------------------------------------
# SIMULACION
# --------------------------------------

primera_iteracion=True
bar = Bar('Processing', max=tiempo_fin_simulacion)

while tiempo_sistema < tiempo_fin_simulacion:

  bar.next()

  agregar_nueva_tarea(lista_tareas,tiempo_sistema,primera_iteracion=primera_iteracion)
  
  # print(f"LISTA DE TAREAS: {list(map(lambda e:e.get_dict(),lista_tareas))}")

  primera_iteracion=False

  actualizar_tiempos_ociosos()

  if hay_una_llegada( lista_tareas, tiempo_sistema):

    tarea_a_resolver = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.Llegada)
    resolver_tarea( tarea_a_resolver ,tiempo_sistema,lista_administradores)
      
  if hay_una_salida(lista_tareas,tiempo_sistema):
    tarea_a_finalizar = obtener_tarea( lista_tareas, tiempo_sistema ,evento=EventoTarea.Salida)
    finalizar_tarea(tarea_a_finalizar,lista_administradores,tiempo_sistema)
      
  tiempo_sistema = incrementar_tiempo_sistema(lista_administradores,tiempo_sistema)

bar.finish()

resultado_simulacion.historico_tareas = historico_tareas
metricas = resultado_simulacion.generar_metricas(lista_tareas)

print(metricas)




    
    
    
    
    
    
    
    
    
    
    
    
