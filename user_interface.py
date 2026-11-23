from datetime import date

from business_logic import (
    Museo,
    buscar_museo,
    nombres_de_museos,
    crear_museo_validado,
    )


# Pide el nombre y devuelve el museo, o None si no existe.
def pedir_museo(museos: list) -> Museo | None:
    nombre = input("Nombre del museo: ")
    try:
        return buscar_museo(nombre, museos)
    except ValueError as error:
        print(error)
        return None
        

# --- Crear un museo ---
def opcion_crear_museo(museos: list):
    print("\n--- Crear museo ---")
    nombre = input("Nombre del museo: ")
    aforo_diario = input("Aforo diario: ")
    año = input("Año de inicio: ")
    mes = input("Mes de inicio (número): ")
    dia = input("Día de inicio: ")

    try:
        museo = crear_museo_validado(nombre, aforo_diario, año, mes, dia,
                                     nombres_de_museos(museos))
        museos.append(museo)
        print("Museo creado, sin días registrados.")
    except ValueError as error:
        print(error)


# --- Registrar el día siguiente ---
def opcion_registrar_dia(museos: list):
    print("\n--- Registrar visitantes del día siguiente ---")
    museo = pedir_museo(museos)
    if museo is None:
        return
    
    try:
        museo.validar_capacidad(1)
    except ValueError as error:
        print(error)
        return

    print(f"Día a registrar: {museo.fecha_siguiente()}")
    dia_guardado = False
    while not dia_guardado:
        try:
            visitantes = museo.validar_visitantes(input("Visitantes del día: "))
            museo.registrar_dia(visitantes)
            dia_guardado = True
        except ValueError as error:
            print(error)
    print("Día registrado.")


# --- Simular días ---
def opcion_simular_dias(museos: list):
    print("\n--- Simular días ---")
    museo = pedir_museo(museos)
    if museo is None:
        return

    try:
        dias = museo.validar_num_dias(input("¿Cuántos días quieres simular? "))
        minimo = museo.validar_visitantes(input("Visitantes mínimos: "))
        maximo = museo.validar_visitantes(input("Visitantes máximos: "))
        museo.validar_rango(minimo, maximo)
        museo.validar_capacidad(dias)
        museo.simular_dias(dias, minimo, maximo)
        print(f"Se simularon {dias} días para {museo.nombre}.")
    except ValueError as error:
        print(error)


# --- Informe de un museo ---
def opcion_informe_museo(museos: list):
    print("\n--- Informe de museo ---")
    museo = pedir_museo(museos)
    if museo is None:
        return

    print(museo.generar_informe(date.today()))



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
            opcion_crear_museo(museos)
        elif opcion == "2":
            opcion_registrar_dia(museos)
        elif opcion == "3":
            opcion_simular_dias(museos)
        elif opcion == "4":
            opcion_informe_museo(museos)
        elif opcion == "5" or opcion == "6":
            print("Esta opción aún no está disponible.")
        elif opcion == "7":
            print("Hasta luego.")
            salir = True
        else:
            print("La opción no es válida.")
