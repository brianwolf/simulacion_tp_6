import generico
import configuracion
import administradores

from generador_tareas import crear_tarea_random
from intervalo_arribo_tarea import proximo_arribo_tarea

# ----------------------------------------------------
# VARIABLES
# ----------------------------------------------------

tiempo = 1
proximo_tiempo_arribo = 0

tiempos_ociosos = { 
    generico.TipoPerfil.JUNIOR: 0,
    generico.TipoPerfil.SEMISENIOR: 0,
    generico.TipoPerfil.SENIOR: 0
}

tareas_encoladas = []
tareas_hechas = []


# ----------------------------------------------------
# METODOS
# ----------------------------------------------------
def hay_salidas() -> bool:
    global tiempo
    return administradores.hay_salidas(tiempo)


def alguien_esta_libre() -> bool:
    return administradores.alguien_esta_libre()


def avanzar_tiempo():
    global tiempo
    tiempo += 1


def resolver_entrada():
    global tareas_encoladas, proximo_tiempo_arribo

    tarea_nueva = crear_tarea_random()
    tareas_encoladas.append(tarea_nueva)


def resolver_tiempo_ocioso():
    global tiempos_ociosos

    tiempos_ociosos[generico.TipoPerfil.JUNIOR] += administradores.obtener_tiempo_ocioso(generico.TipoPerfil.JUNIOR) 
    tiempos_ociosos[generico.TipoPerfil.SEMISENIOR] += administradores.obtener_tiempo_ocioso(generico.TipoPerfil.SEMISENIOR) 
    tiempos_ociosos[generico.TipoPerfil.SENIOR] += administradores.obtener_tiempo_ocioso(generico.TipoPerfil.SENIOR)


def resolver_ponerse_a_trabajar():
    global tareas_encoladas

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
    while tiempo < configuracion.tiempo_simulacion_horas:

        resolver_entrada()

        if alguien_esta_libre():
            resolver_ponerse_a_trabajar()
            resolver_tiempo_ocioso()

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
    print(f'simples: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.SIMPLE, tareas_hechas)))}')
    print('\n')
    
    print('ENCOLADAS:')
    print('\n')
    
    print(f'JUNIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.JUNIOR , tareas_encoladas)))}')
    print(f'SEMISENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SEMISENIOR , tareas_encoladas)))}')
    print(f'SENIOR: {len(list(filter(lambda tarea: tarea.perfil == generico.TipoPerfil.SENIOR , tareas_encoladas)))}')
    print('\n')
    
    print(f'Caoticas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.CAOTICA , tareas_encoladas)))}')
    print(f'Complejas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLEJA , tareas_encoladas)))}')
    print(f'Complicadas: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLICADA , tareas_encoladas)))}')
    print(f'simples: {len(list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.SIMPLE, tareas_encoladas)))}')
    print('\n')
    
    print('TIEMPOS OCIOSOS')
    print('\n')
    print(f'SENIOR: {str(tiempos_ociosos[generico.TipoPerfil.SENIOR]/tiempo)}')
    print(f'SEMISENIOR: {str(tiempos_ociosos[generico.TipoPerfil.SEMISENIOR]/tiempo)}')
    print(f'JUNIOR: {str(tiempos_ociosos[generico.TipoPerfil.JUNIOR]/tiempo)}')
    print('\n')

    # print('TIEMPOS OCIOSOS')
    # print('\n')
    # print(f'CAOTICA: {sum([generico.fecha_a_tiempo_simulacion(tarea.fecha_fin) for tarea in list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.CAOTICA , tareas_hechas))]) / configuracion.tiempo_simulacion_horas}')
    # print(f'COMPLEJO: {sum([generico.fecha_a_tiempo_simulacion(tarea.fecha_fin) for tarea in list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLEJA , tareas_hechas))]) / configuracion.tiempo_simulacion_horas}')
    # print(f'COMPLICADO: {sum([generico.fecha_a_tiempo_simulacion(tarea.fecha_fin) for tarea in list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.COMPLICADA , tareas_hechas))]) / configuracion.tiempo_simulacion_horas}')
    # print(f'SIMPLE: {sum([generico.fecha_a_tiempo_simulacion(tarea.fecha_fin) for tarea in list(filter(lambda tarea: tarea.tipo == generico.TipoTarea.SIMPLE , tareas_hechas))]) / configuracion.tiempo_simulacion_horas}')
    # print('\n')
    

# ----------------------------------------------------
# EJECUCION
# ----------------------------------------------------

if __name__ == "__main__":
    ejecutar_simulacion()