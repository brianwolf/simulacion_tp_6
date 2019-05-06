import random

from generico import ProbabilidadTiempo

# ----------------------------------------------------
# PROBABILIDADES
# ----------------------------------------------------
lista_probabilidades = [
    ProbabilidadTiempo(15, 0.05),
    ProbabilidadTiempo(30, 0.1),
    ProbabilidadTiempo(60, 0.2),
    ProbabilidadTiempo(120,0.15),
    ProbabilidadTiempo(240,0.3),
    ProbabilidadTiempo(480,0.25)
]


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------

def proximo_arribo_tarea() -> int:
    
    numero_aleatorio = random.random()
    i = 0
    while i < len(lista_probabilidades):

        prob_anterior = 0 if i == 0 else prob_anterior + lista_probabilidades[i-1].probabilidad
        prob_siguiente = prob_anterior + lista_probabilidades[i].probabilidad

        if prob_anterior <= numero_aleatorio <= prob_siguiente:
            return lista_probabilidades[i].tiempo
        
        i+=1


# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------
if __name__ == "__main__":

    lista_arribos = []
    while len(lista_arribos) < 1000:
        lista_arribos.append(proximo_arribo_tarea())

    print(lista_arribos)
