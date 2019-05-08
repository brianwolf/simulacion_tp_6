from numpy.random import choice
import json
from datetime import datetime,timedelta
from enum import Enum
import builtins

configuracion = None
FORMATO_SALIDA_FECHA="%d/%m/%yT%H:%M:%SZ"

def print(algo,logging=None):
  if logging or configuracion and configuracion.logging:
    return builtins.print(algo)

class UnidadTiempo(Enum):
    Segundos = "segundos"
    Minutos = "minutos"
    Horas = "horas"

    def llevar_a_minutos(self,un_tiempo:int)->int:
        if self==UnidadTiempo.Segundos:
            return un_tiempo/60
        elif self==UnidadTiempo.Horas:
            return un_tiempo*60
        return un_tiempo
    def llevar_a_horas(self,un_tiempo:int)->int:
        if self==UnidadTiempo.Segundos:
            return un_tiempo/(60*60)
        elif self==UnidadTiempo.Minutos:
            return un_tiempo/60
        return un_tiempo

class ProbabilidadTiempo():
    def __init__(self, tiempo, probabilidad,unidad_tiempo=UnidadTiempo.Horas):
        self.tiempo = round(unidad_tiempo.llevar_a_horas(tiempo))
        self.probabilidad = probabilidad

    def dict(self):
        return self.__dict__()

class Configuracion():
    def __init__(self, configuracion_spec:dict):
        self.logging = configuracion_spec.get("logging",False)
        self.cantidad_juniors = configuracion_spec['cantidad_juniors']
        self.cantidad_semiseniors = configuracion_spec['cantidad_semiseniors']
        self.cantidad_seniors = configuracion_spec['cantidad_seniors']
        self.formato_fecha = configuracion_spec.get("formato_fecha","%d/%m/%y")
        self.fecha_inicial = datetime.strptime(configuracion_spec.get('fecha_inicial',datetime.strftime(datetime.now(),self.formato_fecha)),self.formato_fecha)
        self.unidad_tiempo = UnidadTiempo(configuracion_spec.get('unidad_tiempo',"minutos"))
        self.tiempo_fin_simulacion = self.unidad_tiempo.llevar_a_horas(configuracion_spec['tiempo_fin_simulacion'])
        self.fecha_fin= self.calcular_fecha_fin(self.fecha_inicial,configuracion_spec['tiempo_fin_simulacion'],self.unidad_tiempo)

    def calcular_fecha_fin(self,fecha_inicial:datetime,tiempo_fin:int,unidad_tiempo:UnidadTiempo)->datetime:
        tiempo_fin_minutos = unidad_tiempo.llevar_a_minutos(tiempo_fin)
        dias = round(tiempo_fin_minutos/(8*60))
        meses_laborales = round(dias/20)
        dias_laborales = round(max(meses_laborales*30,dias))
        minutos = tiempo_fin_minutos-dias*8*60
        print(f"CALCULANDO FECHA CON: tm:{tiempo_fin_minutos},d:{dias},ml:{meses_laborales},dl:{dias_laborales},m:{minutos}",logging=self.logging)
        fecha_fin = fecha_inicial+timedelta(days=dias_laborales)+timedelta(minutes=minutos)
        return fecha_fin

    def __str__(self):
        return str(self.dict())

    def dict(self):
        return { 
                "cantidad_juniors" : self.cantidad_juniors,
                "cantidad_semiseniors" : self.cantidad_semiseniors,
                "cantidad_seniors" : self.cantidad_seniors,
                "tiempo_fin_simulacion" : self.tiempo_fin_simulacion,
                "formato_fecha" : self.formato_fecha,
                "fecha_inicial" : datetime.strftime(self.fecha_inicial,FORMATO_SALIDA_FECHA),
                "unidad_tiempo" : UnidadTiempo.Horas.value,
                "fecha_fin": datetime.strftime(self.fecha_fin,FORMATO_SALIDA_FECHA)
               }

# ----------------------------------------------------
# CONFIGURACION DE ARCHIVO
# ----------------------------------------------------
def obtener_configuracion_de_archivo(path)->Configuracion:
    with open(path, encoding='utf-8') as json_file:
        text = json_file.read()
        json_data = json.loads(text)
    return Configuracion(json_data)

configuracion = obtener_configuracion_de_archivo("./configuracion.json")

# ----------------------------------------------------
# CONFIGURACION DE PROBABILIDADES
# ----------------------------------------------------

probabilidades_simple_junior = [
    ProbabilidadTiempo(1, 0.1),
    ProbabilidadTiempo(2, 0.1),
    ProbabilidadTiempo(4,0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
]

probabilidades_simple_semisenior = [
    ProbabilidadTiempo(1, 0.2),
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3)
]

probabilidades_simple_senior = [
    ProbabilidadTiempo(2,0.7),
    ProbabilidadTiempo(4,0.3)
]

probabilidades_complicado_junior = [
    ProbabilidadTiempo(4, 0.1),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
    ProbabilidadTiempo(24, 0.2),
    ProbabilidadTiempo(32,0.1)
]

probabilidades_complicado_semisenior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16,0.3),
    ProbabilidadTiempo(24, 0.2)
]

probabilidades_complicado_senior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.5),
    ProbabilidadTiempo(16,0.3)
]

probabilidades_complejo_semisenior = [
    ProbabilidadTiempo(2, 0.05),
    ProbabilidadTiempo(4, 0.1),
    ProbabilidadTiempo(8, 0.1),
    ProbabilidadTiempo(16,0.2),
    ProbabilidadTiempo(32,0.3),
    ProbabilidadTiempo(48,0.25)
]

probabilidades_complejo_senior = [
    ProbabilidadTiempo(2, 0.2),
    ProbabilidadTiempo(4, 0.3),
    ProbabilidadTiempo(8, 0.2),
    ProbabilidadTiempo(16,0.2),
    ProbabilidadTiempo(32,0.1)
]

probabilidades_caotico_semisenior = [
    ProbabilidadTiempo(4, 0.2),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16, 0.1),
    ProbabilidadTiempo(32,0.3),
    ProbabilidadTiempo(48,0.1)
]

probabilidades_caotico_senior = [
    ProbabilidadTiempo(4, 0.3),
    ProbabilidadTiempo(8, 0.3),
    ProbabilidadTiempo(16, 0.2),
    ProbabilidadTiempo(32,0.2)
]

lista_probabilidades_arribo = [
    ProbabilidadTiempo(15, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.2)
]


def intervalo_de_arribo(tiempo_sistema):
    tiempos = [tp.tiempo for tp in lista_probabilidades_arribo]
    probabilidades = [tp.probabilidad for tp in lista_probabilidades_arribo]

    return choice(tiempos, size=1,p=probabilidades,replace=True)[0]

def obtener_juniors()->int:
    return configuracion.cantidad_juniors

def obtener_semiseniors()->int:
    return configuracion.cantidad_semiseniors

def obtener_seniors()->int:
    return configuracion.cantidad_seniors

def obtener_tiempo_fin_simulacion():
    return configuracion.tiempo_fin_simulacion

def probabilidades_tipo_tarea():
    return [("Caotico",0.07),("Complicado",0.37),("Simple",0.25),("Complejo",0.31)]

def probabilidad_tipo_tarea(un_tipo:str):
    return next(t[1] for t in probabilidades_tipo_tarea() if t[0]==un_tipo)

def tiempos_de_resolucion_probables_de(nombre_perfil,tipo_tarea):
    probabilidades_por_tiempo = globals()[f'probabilidades_{tipo_tarea.lower()}_{nombre_perfil.lower()}']
    return list(map(lambda ppt: (ppt.tiempo,ppt.probabilidad),probabilidades_por_tiempo))
    # return list(map(lambda ppt: (ppt.tiempo//1000,ppt.probabilidad),probabilidades_por_tiempo))

def get_config():
    return configuracion