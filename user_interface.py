from datetime import date

from business_logic import (
    Museo,
    buscar_museo,
    nombres_de_museos,
    crear_museo_validado,
    museo_mayor_asistencia,
    museo_menor_asistencia,
    leer_registros,
    cargar_museos,
    cargar_visitantes,
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


# --- Porcentaje más alto y más bajo ---
def opcion_porcentajes_extremos(museos: list):
    print("\n--- Porcentaje de asistencia más alto y más bajo ---")
    mayor = museo_mayor_asistencia(museos)
    if mayor is None:
        print("Ningún museo tiene días registrados.")
        return

    menor = museo_menor_asistencia(museos)
    print(f"Mayor porcentaje de asistencia: {mayor.nombre}, "
          f"{round(mayor.porcentaje_asistencia(), 2)} %")
    print(f"Menor porcentaje de asistencia: {menor.nombre}, "
          f"{round(menor.porcentaje_asistencia(), 2)} %")


# --- Cargar museos y visitantes desde archivos ---
def leer_archivo(ruta: str) -> list | None:
    try:
        return leer_registros(ruta.strip())
    except UnicodeDecodeError:
        print("El archivo no está guardado en UTF-8.")
        return None
    except OSError:
        print("El archivo no existe.")
        return None


# Muestra las líneas descartadas y cuántos registros se cargaron.
def mostrar_resultado_de_carga(resultado: dict, que_se_cargo: str):
    for descartada in resultado["descartadas"]:
        print(f"Línea {descartada[0]} descartada: {descartada[1]}")
    print(f"Se cargaron {resultado['cargados']} {que_se_cargo}.")


def opcion_cargar_archivos(museos: list):
    print("\n--- Cargar museos y visitantes desde archivos ---")
    if len(museos) > 0:
        print("La carga solo se hace con el programa sin museos.")
        return

    registros_museos = leer_archivo(input("Ruta del archivo de museos: "))
    if registros_museos is None:
        return
    mostrar_resultado_de_carga(cargar_museos(registros_museos, museos), "museos")

    registros_visitantes = leer_archivo(input("Ruta del archivo de visitantes: "))
    if registros_visitantes is None:
        return
    mostrar_resultado_de_carga(cargar_visitantes(registros_visitantes, museos), "días")


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
        elif opcion == "5":
            opcion_porcentajes_extremos(museos)
        elif opcion == "6":
            opcion_cargar_archivos(museos)
        elif opcion == "7":
            print("Hasta luego.")
            salir = True
        else:
            print("La opción no es válida.")


if __name__ == "__main__":
    main()