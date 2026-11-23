# Casos de verificación de la Alternativa E (Red de Museos del Caribe).
#
# Cada caso tiene:
#   id, req (grupo del caso), titulo
#   prep      -> código de una preparación (PREP): lo que se hace antes del caso
#   entradas  -> lo que se teclea en el caso, en orden (cada "|" es un Enter)
#   esperado  -> líneas que deben aparecer en la salida del caso, en ese orden
#   ausente   -> líneas que NO deben aparecer
#   veces     -> líneas que deben aparecer exactamente N veces
#   total_en  -> rango permitido para "Visitantes totales" (simulaciones al azar)
#   menus     -> cuántas veces se muestra el menú durante el caso
#
# Las marcas {HOY}, {AYER}, {ANTE} y sus partes ({HOY_A}, {HOY_M}, {HOY_D}, ...)
# se reemplazan por fechas del computador (fecha del computador). {FALT_*} son textos completos.

REQUISITOS = {
    1: "Crear un museo",
    2: "Registrar los visitantes del día siguiente",
    3: "Simular días",
    4: "El informe de un museo",
    5: "La desviación estándar",
    6: "El día de más y el de menos visitantes",
    7: "Los días en cada nivel de asistencia",
    8: "La racha más larga en asistencia baja",
    9: "Los días sin registrar",
    10: "Varios museos en el mismo programa",
    11: "El porcentaje de asistencia más alto y el más bajo",
    12: "Cargar los museos desde un archivo",
    13: "Cargar los visitantes desde un archivo",
    14: "El menú",
    15: "Límite del calendario (requisito agregado por el equipo)",
}

NO_CREADO = "Museo creado"
NO_HAY = "No hay un museo con ese nombre."
INVALIDA = "La opción no es válida."
SIN_DIAS = "El museo no tiene días registrados."
LIMITE = "El registro no puede pasar del 31 de diciembre de 9999."
NO_UTF8 = "El archivo no está guardado en UTF-8."


# Lista de teclas para crear un museo.
def crear(nombre, aforo, anio, mes, dia):
    return ["1", nombre, str(aforo), str(anio), str(mes), str(dia)]


# Lista de teclas para registrar un día.
def dia(nombre, visitantes):
    return ["2", nombre, str(visitantes)]


CAFE = crear("Museo del Café", 150, 2026, 11, 1)
GALERIA = crear("Galería del Puerto", 100, 2026, 11, 1)

PREP = {
    "P0": ("Programa recién iniciado, sin museos.", []),
    "PC": ("Museo del Café creado por teclado (aforo 150, inicio 2026-11-01), sin días.",
           [CAFE]),
    "PC1": ("Museo del Café creado (aforo 150, inicio 2026-11-01) con un día de 60 visitantes.",
            [CAFE, dia("Museo del Café", 60)]),
    "PCa": ("Casa de la Música creada por teclado (aforo 200, inicio 2026-11-01), sin días.",
            [crear("Casa de la Música", 200, 2026, 11, 1)]),
    "PA": ("Cargar museos.csv y visitantes.csv (archivos del enunciado): Museo del Mar (5 días) "
           "y Casa de la Música (4 días).",
           [["6", "museos.csv", "visitantes.csv"]]),
    "PR": ("Cargar museos.csv y visitantes.csv, y después crear Museo del Café (un día de 60) "
           "y Galería del Puerto (sin días).",
           [["6", "museos.csv", "visitantes.csv"], CAFE, dia("Museo del Café", 60), GALERIA]),
    "PX": ("Cargar museos_pruebas.csv y visitantes_pruebas.csv: los museos de errores y los "
           "museos de análisis (Empates, Rachas, Niveles, Cruce, Futuro, Pasado, ...).",
           [["6", "museos_pruebas.csv", "visitantes_pruebas.csv"]]),
    "PL": ("Museo «Fin» creado por teclado (aforo 10, inicio 9999-12-30), sin días.",
           [crear("Fin", 10, 9999, 12, 30)]),
    "PEX": ("Museo Uno (aforo 100, 50 visitantes) y Museo Dos (aforo 200, 100 visitantes): "
            "empate exacto del 50 %.",
            [crear("Museo Uno", 100, 2026, 11, 1), dia("Museo Uno", 50),
             crear("Museo Dos", 200, 2026, 11, 1), dia("Museo Dos", 100)]),
    "PED": ("Museo Seis (aforo 60, 10 visitantes) y luego Museo Tres (aforo 100; 0, 0 y 50): "
            "empate de 16.67 %, con Seis primero.",
            [crear("Museo Seis", 60, 2026, 11, 1), dia("Museo Seis", 10),
             crear("Museo Tres", 100, 2026, 11, 1), dia("Museo Tres", 0),
             dia("Museo Tres", 0), dia("Museo Tres", 50)]),
    "PEDI": ("Museo Tres (aforo 100; 0, 0 y 50) y luego Museo Seis (aforo 60; 10): "
             "empate de 16.67 %, con Tres primero.",
             [crear("Museo Tres", 100, 2026, 11, 1), dia("Museo Tres", 0),
              dia("Museo Tres", 0), dia("Museo Tres", 50),
              crear("Museo Seis", 60, 2026, 11, 1), dia("Museo Seis", 10)]),
    "PSR": ("Museo Diez Mil (aforo 10000, 3333 visitantes) y Museo Tres Plazas (aforo 3, "
            "1 visitante): 33.33 % y 33.333… %.",
            [crear("Museo Diez Mil", 10000, 2026, 11, 1), dia("Museo Diez Mil", 3333),
             crear("Museo Tres Plazas", 3, 2026, 11, 1), dia("Museo Tres Plazas", 1)]),
}

CASOS = []


# Agrega un caso a la lista CASOS.
def caso(id, req, titulo, prep, entradas, esperado, ausente="", veces=None, total_en=None, menus=None):
    def trozos(t):
        return [("" if x == "<ENTER>" else x) for x in t.split("|")] if t != "" else []
    CASOS.append(dict(
        id=id, req=req, titulo=titulo, prep=prep,
        entradas=trozos(entradas), esperado=trozos(esperado), ausente=trozos(ausente),
        veces=veces or {}, total_en=total_en, menus=menus,
    ))


# ---------------------------------------------------------------- Crear un museo
caso("C01-01", 1, "Museo válido: se crea sin días registrados", "P0",
     "1|Museo del Café|150|2026|11|1|4|Museo del Café",
     "Museo creado, sin días registrados.|Museo: Museo del Café|Aforo diario: 150|" + SIN_DIAS,
     ausente="Días registrados:")
caso("C01-02", 1, "Aforo 0", "P0", "1|Museo A|0|2026|11|1|4|Museo A",
     "El aforo diario debe ser de al menos un visitante.|" + NO_HAY, ausente=NO_CREADO)
caso("C01-03", 1, "Aforo escrito como ciento cincuenta", "P0",
     "1|Museo A|ciento cincuenta|2026|11|1|4|Museo A",
     "El aforo diario debe ser un número entero.|" + NO_HAY, ausente=NO_CREADO)
caso("C01-04", 1, "Aforo con decimales (150.5)", "P0", "1|Museo A|150.5|2026|11|1",
     "El aforo diario debe ser un número entero.", ausente=NO_CREADO)
caso("C01-05", 1, "Aforo negativo (-5)", "P0", "1|Museo A|-5|2026|11|1",
     "El aforo diario debe ser de al menos un visitante.", ausente=NO_CREADO)
caso("C01-06", 1, "Aforo en el límite: 1 visitante", "P0", "1|Museo Mínimo|1|2026|11|1|4|Museo Mínimo",
     "Museo creado, sin días registrados.|Aforo diario: 1")
caso("C01-07", 1, "Nombre vacío", "P0", "1|<ENTER>|150|2026|11|1",
     "El nombre no puede estar vacío.", ausente=NO_CREADO)
caso("C01-08", 1, "Nombre solo con espacios", "P0", "1|   |150|2026|11|1",
     "El nombre no puede estar vacío.", ausente=NO_CREADO)
caso("C01-09", 1, "Nombre con espacios al inicio y al final: se guarda sin ellos", "P0",
     "1|  Museo Sin Espacios  |100|2026|11|1|4|Museo Sin Espacios",
     "Museo creado, sin días registrados.|Museo: Museo Sin Espacios")
caso("C01-10", 1, "Nombre repetido: el museo que existía conserva sus datos", "PCa",
     "1|Casa de la Música|210|2026|11|1|4|Casa de la Música",
     "Ya existe un museo con ese nombre.|Museo: Casa de la Música|Aforo diario: 200",
     ausente=NO_CREADO + "|Aforo diario: 210")
caso("C01-11", 1, "Nombre repetido escrito con espacios alrededor", "PCa",
     "1| Casa de la Música |210|2026|11|1", "Ya existe un museo con ese nombre.", ausente=NO_CREADO)
caso("C01-12", 1, "Fecha 31 de noviembre de 2026", "P0", "1|Museo A|150|2026|11|31",
     "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-13", 1, "Mes escrito como noviembre", "P0", "1|Museo A|150|2026|noviembre|1",
     "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-14", 1, "Año escrito con letras", "P0", "1|Museo A|150|dos mil|11|1",
     "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-15", 1, "Día escrito con letras", "P0", "1|Museo A|150|2026|11|primero",
     "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-16", 1, "Día 0", "P0", "1|Museo A|150|2026|11|0", "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-17", 1, "Mes 13", "P0", "1|Museo A|150|2026|13|1", "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-18", 1, "29 de febrero de un año no bisiesto (2027)", "P0", "1|Museo A|150|2027|2|29",
     "La fecha no es válida.", ausente=NO_CREADO)
caso("C01-19", 1, "29 de febrero de un año bisiesto (2028): es válida", "P0", "1|Museo A|150|2028|2|29",
     "Museo creado, sin días registrados.")
caso("C01-20", 1, "Orden de las condiciones: aforo 0 y fecha 31 de noviembre, avisa solo del aforo", "P0",
     "1|Museo A|0|2026|11|31", "El aforo diario debe ser de al menos un visitante.",
     ausente="La fecha no es válida.|" + NO_CREADO)
caso("C01-21", 1, "Orden: nombre vacío, aforo 0 y fecha inválida, avisa solo del nombre", "P0",
     "1|<ENTER>|0|2026|11|31", "El nombre no puede estar vacío.",
     ausente="El aforo diario|La fecha no es válida.")
caso("C01-22", 1, "Orden: nombre repetido y aforo 0, avisa solo del nombre", "PCa",
     "1|Casa de la Música|0|2026|11|1", "Ya existe un museo con ese nombre.",
     ausente="El aforo diario")
caso("C01-23", 1, "Orden: aforo no entero y fecha inválida, avisa solo del aforo", "P0",
     "1|Museo A|abc|2026|11|31", "El aforo diario debe ser un número entero.",
     ausente="La fecha no es válida.")

# ---------------------------------------------------------------- Registrar el día siguiente
caso("C02-01", 2, "Día válido: se muestra la fecha y se registra", "PC",
     "2|Museo del Café|60|4|Museo del Café",
     "Día a registrar: 2026-11-01|Día registrado.|Días registrados: 1|Visitantes totales: 60")
caso("C02-02", 2, "Visitantes escritos como x: avisa y vuelve a leerlos", "PC",
     "2|Museo del Café|x|60",
     "Día a registrar: 2026-11-01|Los visitantes deben ser un número entero.|Día registrado.",
     veces={"Día a registrar:": 1})
caso("C02-03", 2, "151 visitantes (más que el aforo): avisa y vuelve a leerlos", "PC",
     "2|Museo del Café|151|60", "Los visitantes van de 0 a 150.|Día registrado.")
caso("C02-04", 2, "-1 visitantes: avisa y vuelve a leerlos", "PC",
     "2|Museo del Café|-1|60", "Los visitantes van de 0 a 150.|Día registrado.")
caso("C02-05", 2, "Cuatro intentos seguidos: x, 151, -1 y 60", "PC",
     "2|Museo del Café|x|151|-1|60|4|Museo del Café",
     "Los visitantes deben ser un número entero.|Los visitantes van de 0 a 150.|"
     "Los visitantes van de 0 a 150.|Día registrado.|Días registrados: 1|Visitantes totales: 60",
     veces={"Día registrado.": 1})
caso("C02-06", 2, "Visitantes vacíos (solo Enter)", "PC", "2|Museo del Café|<ENTER>|60",
     "Los visitantes deben ser un número entero.|Día registrado.")
caso("C02-07", 2, "Visitantes decimales (60.5)", "PC", "2|Museo del Café|60.5|60",
     "Los visitantes deben ser un número entero.|Día registrado.")
caso("C02-08", 2, "Límites: 0 visitantes y 150 visitantes (el aforo) son válidos", "PC",
     "2|Museo del Café|0|2|Museo del Café|150|4|Museo del Café",
     "Día registrado.|Día registrado.|Días registrados: 2|Visitantes totales: 150",
     ausente="Los visitantes van de")
caso("C02-09", 2, "El día siguiente avanza con cada registro", "PC",
     "2|Museo del Café|60|2|Museo del Café|70",
     "Día a registrar: 2026-11-01|Día registrado.|Día a registrar: 2026-11-02|Día registrado.")
caso("C02-10", 2, "Cambio de año: tres días desde el 30 de diciembre, el siguiente es 2027-01-02", "PX",
     "2|Museo Cruce|5", "Día a registrar: 2027-01-02|Día registrado.")
caso("C02-11", 2, "Museo inexistente: avisa y no lee los visitantes", "PC",
     "2|Museo del Banano|60", NO_HAY, ausente="Día a registrar:", veces={INVALIDA: 1})
caso("C02-12", 2, "Nombre en minúsculas no coincide", "PC", "2|museo del café|60",
     NO_HAY, ausente="Día a registrar:")
caso("C02-13", 2, "Nombre sin tilde no coincide", "PC", "2|Museo del Cafe|60",
     NO_HAY, ausente="Día a registrar:")
caso("C02-14", 2, "Nombre con espacios al inicio y al final sí coincide", "PC",
     "2| Museo del Café |60", "Día a registrar: 2026-11-01|Día registrado.")
caso("C02-15", 2, "Sin ningún museo en el programa", "P0", "2|Museo del Café|60",
     NO_HAY, veces={INVALIDA: 1})

# ---------------------------------------------------------------- Simular días
caso("C03-01", 3, "Tres días entre 75 y 150: se agregan tres días", "PC",
     "3|Museo del Café|3|75|150|4|Museo del Café",
     "Se simularon 3 días para Museo del Café.|Días registrados: 3", total_en=(225, 450))
caso("C03-02", 3, "Cincuenta días entre 75 y 150", "PC",
     "3|Museo del Café|50|75|150|4|Museo del Café",
     "Se simularon 50 días para Museo del Café.|Días registrados: 50", total_en=(3750, 7500))
caso("C03-03", 3, "Mínimo igual al máximo: el resultado es exacto", "PC",
     "3|Museo del Café|4|100|100|4|Museo del Café",
     "Se simularon 4 días para Museo del Café.|Días registrados: 4|Visitantes totales: 400|"
     "Promedio de visitantes por día: 100.0|Desviación estándar: 0.0")
caso("C03-04", 3, "Límites 0 y 0", "PC", "3|Museo del Café|2|0|0|4|Museo del Café",
     "Días registrados: 2|Visitantes totales: 0")
caso("C03-05", 3, "Límites 150 y 150 (el aforo)", "PC", "3|Museo del Café|2|150|150|4|Museo del Café",
     "Días registrados: 2|Visitantes totales: 300")
caso("C03-06", 3, "Los días simulados se agregan después de los registrados", "PC1",
     "3|Museo del Café|2|100|100|4|Museo del Café",
     "Días registrados: 3|Visitantes totales: 260|Último día registrado: 2026-11-03")
caso("C03-07", 3, "Número de días escrito como tres: no lee el mínimo ni el máximo", "PC",
     "3|Museo del Café|tres|75|150|4|Museo del Café",
     "El número de días debe ser un número entero.|" + SIN_DIAS,
     ausente="Se simularon", veces={INVALIDA: 2})
caso("C03-08", 3, "Cero días: no lee el mínimo ni el máximo", "PC",
     "3|Museo del Café|0|75|150|4|Museo del Café",
     "Se debe simular al menos un día.|" + SIN_DIAS, ausente="Se simularon", veces={INVALIDA: 2})
caso("C03-09", 3, "Días negativos", "PC", "3|Museo del Café|-2|75|150|4|Museo del Café",
     "Se debe simular al menos un día.|" + SIN_DIAS, ausente="Se simularon", veces={INVALIDA: 2})
caso("C03-10", 3, "Mínimo x: no lee el máximo", "PC", "3|Museo del Café|3|x|150|4|Museo del Café",
     "Los visitantes deben ser un número entero.|" + SIN_DIAS, ausente="Se simularon", veces={INVALIDA: 1})
caso("C03-11", 3, "Mínimo -1: no lee el máximo", "PC", "3|Museo del Café|3|-1|150|4|Museo del Café",
     "Los visitantes van de 0 a 150.|" + SIN_DIAS, ausente="Se simularon", veces={INVALIDA: 1})
caso("C03-12", 3, "Mínimo 151 (más que el aforo)", "PC", "3|Museo del Café|3|151|150|4|Museo del Café",
     "Los visitantes van de 0 a 150.|" + SIN_DIAS, ausente="Se simularon", veces={INVALIDA: 1})
caso("C03-13", 3, "Máximo x", "PC", "3|Museo del Café|3|75|x|4|Museo del Café",
     "Los visitantes deben ser un número entero.|" + SIN_DIAS, ausente="Se simularon")
caso("C03-14", 3, "Máximo -1", "PC", "3|Museo del Café|3|75|-1|4|Museo del Café",
     "Los visitantes van de 0 a 150.|" + SIN_DIAS, ausente="Se simularon")
caso("C03-15", 3, "Máximo 151", "PC", "3|Museo del Café|3|75|151|4|Museo del Café",
     "Los visitantes van de 0 a 150.|" + SIN_DIAS, ausente="Se simularon")
caso("C03-16", 3, "Mínimo 112 y máximo 75: el mínimo no puede ser mayor", "PC",
     "3|Museo del Café|3|112|75|4|Museo del Café",
     "El mínimo no puede ser mayor que el máximo.|" + SIN_DIAS, ausente="Se simularon")
caso("C03-17", 3, "Museo inexistente: no lee ningún dato", "PC", "3|Museo del Banano|8|75|150",
     NO_HAY, ausente="Se simularon", veces={INVALIDA: 3})
caso("C03-18", 3, "Sin ningún museo en el programa", "P0", "3|Museo del Café|8|75|150",
     NO_HAY, veces={INVALIDA: 3})
caso("C03-19", 3, "Se pueden obtener los dos extremos: 200 días entre 99 y 100", "PC",
     "3|Museo del Café|200|99|100|4|Museo del Café",
     "Se simularon 200 días para Museo del Café.|Días registrados: 200", total_en=(19801, 19999))

# ---------------------------------------------------------------- El informe
caso("C04-01", 4, "Museo del Mar: informe completo", "PA", "4|Museo del Mar",
     "Museo: Museo del Mar|Aforo diario: 500|Días registrados: 5|Visitantes totales: 1420|"
     "Promedio de visitantes por día: 284.0|Porcentaje de asistencia: 56.8 %|"
     "Desviación estándar: 145.68|Día de más visitantes: 2026-11-04|"
     "Día de menos visitantes: 2026-11-03|Días en asistencia baja: 2|Días en asistencia media: 0|"
     "Días en asistencia alta: 2|Días en asistencia plena: 1|"
     "Racha más larga en asistencia baja: 2 días (empezó el 2026-11-02)|"
     "Último día registrado: 2026-11-05|Días sin registrar: {FALT_MAR}")
caso("C04-02", 4, "Casa de la Música: informe completo", "PA", "4|Casa de la Música",
     "Museo: Casa de la Música|Aforo diario: 200|Días registrados: 4|Visitantes totales: 440|"
     "Promedio de visitantes por día: 110.0|Porcentaje de asistencia: 55.0 %|"
     "Desviación estándar: 49.5|Día de más visitantes: 2026-11-04|"
     "Día de menos visitantes: 2026-11-01|Días en asistencia baja: 1|Días en asistencia media: 1|"
     "Días en asistencia alta: 1|Días en asistencia plena: 1|"
     "Racha más larga en asistencia baja: 1 día (empezó el 2026-11-01)|"
     "Último día registrado: 2026-11-04")
caso("C04-03", 4, "Galería del Puerto sin días: solo nombre, aforo y aviso", "PR", "4|Galería del Puerto",
     "Museo: Galería del Puerto|Aforo diario: 100|" + SIN_DIAS,
     ausente="Días registrados:|Visitantes totales|Promedio|Porcentaje|Desviación|Racha")
caso("C04-04", 4, "Un porcentaje de 64 se muestra como 64.0 y no como 64.00", "P0",
     "1|Museo Entero|100|2026|11|1|2|Museo Entero|64|4|Museo Entero",
     "Promedio de visitantes por día: 64.0|Porcentaje de asistencia: 64.0 %", ausente="64.00")
caso("C04-05", 4, "Redondeo a dos decimales (promedio 33.33, porcentaje 11.11)", "PX",
     "4|Museo Decimales",
     "Promedio de visitantes por día: 33.33|Porcentaje de asistencia: 11.11 %|Desviación estándar: 47.14")
caso("C04-06", 4, "Aforo completo todos los días: 100.0 %", "PX", "4|Museo Lleno",
     "Visitantes totales: 200|Promedio de visitantes por día: 100.0|Porcentaje de asistencia: 100.0 %")
caso("C04-07", 4, "Museo inexistente", "PA", "4|Museo del Banano", NO_HAY, ausente="Museo:")

# ---------------------------------------------------------------- Desviación estándar
caso("C05-01", 5, "Museo del Mar: 145.68", "PA", "4|Museo del Mar", "Desviación estándar: 145.68")
caso("C05-02", 5, "Casa de la Música: 49.5", "PA", "4|Casa de la Música", "Desviación estándar: 49.5")
caso("C05-03", 5, "Un solo día registrado: 0.0", "PC1", "4|Museo del Café", "Desviación estándar: 0.0")
caso("C05-04", 5, "Todos los días iguales: 0.0", "PX", "4|Museo Plano", "Desviación estándar: 0.0")
caso("C05-05", 5, "Valores 100, 0 y 0: 47.14", "PX", "4|Museo Decimales", "Desviación estándar: 47.14")
