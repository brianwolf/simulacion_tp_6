from administrador_tareas import Tarea,DificultadTarea,generar_tarea_aleatoria
import random
from file_manager import create_json_file,converter
from datetime import datetime
from datetime import timedelta  
from app import hay_una_llegada,hay_una_salida,EventoTarea,obtener_tarea,resolver_tarea,finalizar_tarea,realizar_simulacion
import json

MAX_CANT_MINUTOS=10000


def guardar_datos_simulacion(data):
    create_json_file('/nuevos_datos','nueva_data_simulacion',data)

def get_safe_date(reference_date,some_hours,min_date):
    now = datetime.now()
    new_date =  reference_date + timedelta(hours = some_hours)
    return (min_date+timedelta(hours = some_hours)) if new_date>now else new_date

def completar_fechas(tarea,lista_inicial):
    lista_creaciones = list(map(lambda t:datetime.strptime(t.fecha_creacion,"%d/%m/%y"),lista_inicial))

    max_date = max(lista_creaciones)
    min_date = min(lista_creaciones)

    now = datetime.now()
    reference_date = random.choice([max_date,min_date])
    reference_date = min(now,reference_date)
    min_date_hard = datetime.strptime("01/01/18","%d/%m/%y")

    tarea.fecha_creacion = get_safe_date(reference_date,tarea.fecha_creacion,min_date_hard)
    tarea.fecha_inicio = get_safe_date(reference_date,tarea.fecha_inicio,min_date_hard)
    tarea.fecha_fin = get_safe_date(reference_date,int(tarea.fecha_fin),min_date_hard)

    return tarea


def crear_nueva_tarea(tiempo)->Tarea:
    tarea:Tarea = generar_tarea_aleatoria(tiempo)
    tarea.fecha_creacion = int(random.choice(range(tiempo,MAX_CANT_MINUTOS)))
    return tarea

def hacer_simulacion(lista_tareas):
    return realizar_simulacion(lista_tareas,simulacion_principal=False)

def get_valid_tasks(tareas):
    new_list = []
    for t in tareas:
        if(not isinstance(t.fecha_inicio, datetime) or not isinstance(t.fecha_fin, datetime)):
            continue
        new_list.append(t)
    return new_list

def crear_nuevos_datos():

    lista_mapas = cargar_datos_simulacion()

    lista_tareas_inicial = list(map(lambda m: Tarea(m),lista_mapas))
    nuevas_tareas = []

    for t in range(MAX_CANT_MINUTOS):
        nueva_tarea = crear_nueva_tarea(t)
        nuevas_tareas.append(nueva_tarea)

    nuevas_tareas = hacer_simulacion(nuevas_tareas)

    nuevas_tareas = list(map(lambda t: completar_fechas(t,lista_tareas_inicial),nuevas_tareas))

    nuevas_tareas = get_valid_tasks(nuevas_tareas)
    
    guardar_datos_simulacion(nuevas_tareas)

def cargar_datos_simulacion():
    return [
    {
      "tipo_tarea": "Caotico",
      "perfil": "senior",
      "fecha_creacion": "09/04/19",

      "fecha_inicio": "19/04/19",
      "fecha_fin": "22/04/19"
    },
    {
      "tipo_tarea": "Caotico",
      "perfil": "senior",
      "fecha_creacion": "10/04/19",
      "fecha_inicio": "15/04/19",
      "fecha_fin": "19/04/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "senior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "01/04/19",
      "fecha_fin": "08/04/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "12/03/19",
      "fecha_fin": "15/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "junior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "13/03/19",
      "fecha_fin": "14/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "junior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "17/03/19",
      "fecha_fin": "19/03/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "25/03/19",
      "fecha_inicio": "25/03/19",
      "fecha_fin": "27/03/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "26/04/19",
      "fecha_inicio": "26/04/19",
      "fecha_fin": "29/04/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "20/03/19",
      "fecha_inicio": "26/04/19",
      "fecha_fin": "26/04/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "01/03/19",
      "fecha_inicio": "01/04/19",
      "fecha_fin": "02/04/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "25/03/19",
      "fecha_inicio": "01/04/19",
      "fecha_fin": "04/04/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "25/03/19",
      "fecha_inicio": "28/03/19",
      "fecha_fin": "29/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "semisenior",
      "fecha_creacion": "27/03/19",
      "fecha_inicio": "28/03/19",
      "fecha_fin": "01/03/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "senior",
      "fecha_creacion": "27/03/19",
      "fecha_inicio": "28/03/19",
      "fecha_fin": "12/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "28/03/19",
      "fecha_inicio": "28/03/19",
      "fecha_fin": "02/04/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "senior",
      "fecha_creacion": "21/03/19",
      "fecha_inicio": "26/03/19",
      "fecha_fin": "27/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "junior",
      "fecha_creacion": "27/11/18",
      "fecha_inicio": "21/03/19",
      "fecha_fin": "23/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "semisenior",
      "fecha_creacion": "20/03/19",
      "fecha_inicio": "20/03/19",
      "fecha_fin": "22/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "semisenior",
      "fecha_creacion": "27/03/19",
      "fecha_inicio": "20/03/19",
      "fecha_fin": "20/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "07/01/19",
      "fecha_inicio": "20/03/19",
      "fecha_fin": "21/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "junior",
      "fecha_creacion": "29/11/18",
      "fecha_inicio": "19/03/19",
      "fecha_fin": "08/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "junior",
      "fecha_creacion": "25/03/19",
      "fecha_inicio": "19/03/19",
      "fecha_fin": "27/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "18/03/19",
      "fecha_inicio": "19/03/19",
      "fecha_fin": "25/03/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "senior",
      "fecha_creacion": "19/03/19",
      "fecha_inicio": "19/03/19",
      "fecha_fin": "20/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "junior",
      "fecha_creacion": "28/11/18",
      "fecha_inicio": "18/03/19",
      "fecha_fin": "21/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "semisenior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "17/03/19",
      "fecha_fin": "18/03/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "senior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "14/03/19",
      "fecha_fin": "19/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "junior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "13/03/19",
      "fecha_fin": "18/03/19"
    },
    {
      "tipo_tarea": "Simple",
      "perfil": "junior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "12/03/19",
      "fecha_fin": "13/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "junior",
      "fecha_creacion": "13/03/19",
      "fecha_inicio": "12/03/19",
      "fecha_fin": "03/04/19"
    },
    {
      "tipo_tarea": "Compleja",
      "perfil": "semisenior",
      "fecha_creacion": "12/03/19",
      "fecha_inicio": "12/03/19",
      "fecha_fin": "17/03/19"
    },
    {
      "tipo_tarea": "Complicado",
      "perfil": "senior",
      "fecha_creacion": "25/03/19",
      "fecha_inicio": "08/03/19",
      "fecha_fin": "08/03/19"
    }
  ]
  
if __name__ == "__main__":
    crear_nuevos_datos()