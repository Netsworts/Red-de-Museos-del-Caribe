from Museo_Logica import crear_museo_validado


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


def main():
    museos = []

    while True:
        print("\n=====================================")
        print("Programa de registro de museos")
        print("=====================================")
        print("1. Crear museo")
        print("7. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            menu_crear(museos)
        elif opcion == "7":
            print("Hasta luego.")
            break
        else:
            print("La opción no es válida.")


if __name__ == "__main__":
    main()
