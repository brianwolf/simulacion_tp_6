from numpy.random import choice

class ProbabilidadTiempo():
    def __init__(self, tiempo, probabilidad):
        self.tiempo = round(tiempo/60)
        self.probabilidad = probabilidad

    def dict(self):
        return self.__dict__()

# ----------------------------------------------------
# CONFIGURACION DE PROBABILIDADES
# ----------------------------------------------------

probabilidades_simple_junior = [
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.1),
    ProbabilidadTiempo(240, 0.1),
    ProbabilidadTiempo(240,0.25),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_simple_semisenior = [
    ProbabilidadTiempo(30, 0.3),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(240, 0.3),
    ProbabilidadTiempo(480,0.2)
]

probabilidades_simple_senior = [
    ProbabilidadTiempo(240,0.7),
    ProbabilidadTiempo(480,0.3)
]

probabilidades_complicado_junior = [
    ProbabilidadTiempo(20, 0.05),
    ProbabilidadTiempo(30, 0.2),
    ProbabilidadTiempo(60, 0.3),
    ProbabilidadTiempo(120,0.10),
    ProbabilidadTiempo(240,0.1),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complicado_semisenior = [
    ProbabilidadTiempo(30, 0.2),
    ProbabilidadTiempo(60, 0.1),
    ProbabilidadTiempo(120,0.10),
    ProbabilidadTiempo(240,0.35),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complicado_senior = [
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complejo_semisenior = [
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.1),
    ProbabilidadTiempo(120,0.2),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_complejo_senior = [
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]

probabilidades_caotico_semisenior = [
    ProbabilidadTiempo(60, 0.3),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240, 0.05),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.20)
]

probabilidades_caotico_senior = [
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.1),
    ProbabilidadTiempo(240,0.2),
    ProbabilidadTiempo(240, 0.15),
    ProbabilidadTiempo(480,0.25)
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
    return 3

def obtener_semiseniors()->int:
    return 2

def obtener_seniors()->int:
    return 1

def obtener_tiempo_fin_simulacion():
    return 10000

def probabilidades_tipo_tarea():
    return [("Caotico",0.07),("Complicado",0.37),("Simple",0.25),("Complejo",0.31)]

def probabilidad_tipo_tarea(un_tipo:str):
    return next(t[1] for t in probabilidades_tipo_tarea() if t[0]==un_tipo)

def tiempos_de_resolucion_probables_de(nombre_perfil,tipo_tarea):
    probabilidades_por_tiempo = globals()[f'probabilidades_{tipo_tarea.lower()}_{nombre_perfil.lower()}']
    return list(map(lambda ppt: (ppt.tiempo,ppt.probabilidad),probabilidades_por_tiempo))
    # return list(map(lambda ppt: (ppt.tiempo//1000,ppt.probabilidad),probabilidades_por_tiempo))