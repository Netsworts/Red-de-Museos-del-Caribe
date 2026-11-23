from business_logic import (
    buscar_museo,
    crear_museo_validado,
    )

def pedir_museo(museos):
    nombre = input("Nombre del museo: ")
    try:
        return buscar_museo(nombre, museos)
    except ValueError as error:
        print(error)
        return None
        

def menu_crear(museos):
    print("\n--- Crear museo ---")
    nombres_existentes = []
    for museo in museos:
        nombres_existentes.append(museo.nombre)

    nombre = input("Nombre del museo: ")
    aforo_diario = input("Aforo diario: ")
    año = input("Año de inicio: ")
    mes = input("Mes de inicio (número): ")
    dia = input("Día de inicio: ")

    try:
        museo = crear_museo_validado(nombre, aforo_diario, año, mes, dia,
                                     nombres_existentes)
    except ValueError as error:
        print(error)
        return

    museos.append(museo)
    print("Museo creado, sin días registrados.")


def menu_registrar(museos):
    print("\n--- Registrar visitantes del día siguiente ---")
    museo = pedir_museo(museos)
    if museo is None:
        return

    print(f"Día a registrar: {museo.fecha_siguiente()}")
    while True:
        try:
            visitantes = museo.validar_visitantes(input("Visitantes del día: "))
            break
        except ValueError as error:
            print(error)

    museo.registrar_dia(visitantes)
    print("Día registrado.")


def menu_simular(museos):
    print("\n--- Simular días ---")
    museo = pedir_museo(museos)
    if museo is None:
        return

    try:
        dias = museo.validar_num_dias(input("¿Cuántos días quieres simular? "))
        minimo = museo.validar_visitantes(input("Visitantes mínimos: "))
        maximo = museo.validar_visitantes(input("Visitantes máximos: "))
        museo.validar_rango(minimo, maximo)
    except ValueError as error:
        print(error)
        return

    museo.simular_dias(dias, minimo, maximo)
    print(f"Se simularon {dias} días para {museo.nombre}.")


def menu_informe(museos):
    print("\n--- Informe de museo ---")
    museo = pedir_museo(museos)
    if museo is None:
        return

    print(museo.generar_informe())


# --- Menú principal ---
def main():
    OPCIONES = [
        "Crear museo",
        "Registrar visitantes del día siguiente",
        "Simular días",
        "Informe de museo",
        "Museo con mayor y menor porcentaje de asistencia",
        "Cargar museos y visitantes desde archivos",
        "Salir",
    ]
    museos = []
    salir = False

    while not salir:
        print("\n=====================================")
        print("Programa de registro de museos")
        print("=====================================")
        for indice in range(len(OPCIONES)):
            print(f"{indice + 1}. {OPCIONES[indice]}")    # el menú numera desde 1
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            menu_crear(museos)
        elif opcion == "2":
            menu_registrar(museos)
        elif opcion == "3":
            menu_simular(museos)
        elif opcion == "4":
            menu_informe(museos)
        elif opcion == "5" or opcion == "6":
            print("Esta opción aún no está disponible.")
        elif opcion == "7":
            print("Hasta luego.")
            salir = True
        else:
            print("La opción no es válida.")
