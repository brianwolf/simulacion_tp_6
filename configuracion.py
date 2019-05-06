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

def tiempos_de_resolucion_probables_de(nombre_perfil):
    if nombre_perfil=="junior":
        return [(48	,2/9),(72	,1/9),(24	,1/9),(120	,1/9),(696	,1/9),(456	,2/9),(192	,1/9)]
    elif nombre_perfil=="semisenior":
        return [(72	,3/9),(24	,2/9),(120	,1/9),(0	,1/9),(48	,2/9)]
    elif nombre_perfil=="senior":
        return [(24	,4/13),(168	,1/13),(120	,1/13),(144	,1/13),(72	,2/13),(0	,1/13),(336	,1/13),(96	,2/13)]