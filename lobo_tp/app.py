import generico
import configuracion
import administradores

from generador_tareas import crear_tarea_random
from intervalo_arribo_tarea import proximo_arribo_tarea

# ----------------------------------------------------
# VARIABLES
# ----------------------------------------------------

tiempo = 0
proximo_tiempo_arribo = 0

tareas_encoladas = []
tareas_hechas = []


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------
def hay_entrada() -> bool:
    # global tiempo, proximo_tiempo_arribo
    # return tiempo == proximo_tiempo_arribo
    return True


def hay_salidas() -> bool:
    global tiempo
    return administradores.hay_salidas(tiempo)


def alguien_esta_libre():
    return administradores.alguien_esta_libre()


def avanzar_tiempo():
    global tiempo
    tiempo += 1


def resolver_entrada():
    global tareas_encoladas, proximo_tiempo_arribo

    tarea_nueva = crear_tarea_random()
    tareas_encoladas.append(tarea_nueva)


def resolver_ponerse_a_trabajar():
    global tareas_encoladas

    if not tareas_encoladas:
        return

    for tarea_a_resolver in tareas_encoladas:
        
        if administradores.alguien_puede_resolver(tarea_a_resolver):
            administradores.poner_a_resolver(tarea_a_resolver)
            tareas_encoladas.remove(tarea_a_resolver)


def resolver_salida():
    global tareas_hechas

    resueltas = administradores.resolver_salidas(tiempo)
    tareas_hechas.extend(resueltas)


def ejecutar_simulacion():
    global proximo_tiempo_arribo, tiempo
    proximo_tiempo_arribo = 0

    while tiempo < configuracion.tiempo_simulacion_horas:

        # if proximo_tiempo_arribo == 0:
        #     proximo_tiempo_arribo = proximo_arribo_tarea()

        if hay_entrada():
            resolver_entrada()

        if alguien_esta_libre():
            resolver_ponerse_a_trabajar()

        if hay_salidas():
            resolver_salida()

        avanzar_tiempo()
    print('\n')

    print(f'HECHAS: {len(tareas_hechas)}')
    print(f'ENCOLADAS: {len(tareas_encoladas)}')
    print('\n')
    
    print('HECHAS:')
    print('\n')
    
    print(f'JUNIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.JUNIOR , tareas_hechas)))}')
    print(f'SEMISENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SEMISENIOR , tareas_hechas)))}')
    print(f'SENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SENIOR , tareas_hechas)))}')
    print('\n')
    
    print(f'Caoticas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.CAOTICA , tareas_hechas)))}')
    print(f'Complejas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLEJA , tareas_hechas)))}')
    print(f'Complicadas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLICADA , tareas_hechas)))}')
    print(f'simples: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.FACIL, tareas_hechas)))}')
    print('\n')
    
    print('ACOLADAS:')
    print('\n')
    
    print(f'JUNIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.JUNIOR , tareas_encoladas)))}')
    print(f'SEMISENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SEMISENIOR , tareas_encoladas)))}')
    print(f'SENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SENIOR , tareas_encoladas)))}')
    print('\n')
    
    print(f'Caoticas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.CAOTICA , tareas_encoladas)))}')
    print(f'Complejas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLEJA , tareas_encoladas)))}')
    print(f'Complicadas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLICADA , tareas_encoladas)))}')
    print(f'simples: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.FACIL, tareas_encoladas)))}')
    print('\n')
    


# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------

if __name__ == "__main__":
    ejecutar_simulacion()