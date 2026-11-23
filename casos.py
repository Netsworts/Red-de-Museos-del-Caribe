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

# ---------------------------------------------------------------- Día de más y de menos visitantes
caso("C06-01", 6, "Museo del Mar", "PA", "4|Museo del Mar",
     "Día de más visitantes: 2026-11-04|Día de menos visitantes: 2026-11-03")
caso("C06-02", 6, "Casa de la Música", "PA", "4|Casa de la Música",
     "Día de más visitantes: 2026-11-04|Día de menos visitantes: 2026-11-01")
caso("C06-03", 6, "Empates en el máximo y en el mínimo: gana el primero", "PX", "4|Museo Empates",
     "Día de más visitantes: 2026-11-02|Día de menos visitantes: 2026-11-04")
caso("C06-04", 6, "Todos los días iguales: el primer día es el máximo y el mínimo", "PX", "4|Museo Plano",
     "Día de más visitantes: 2026-11-01|Día de menos visitantes: 2026-11-01")
caso("C06-05", 6, "Un solo día registrado", "PC1", "4|Museo del Café",
     "Día de más visitantes: 2026-11-01|Día de menos visitantes: 2026-11-01")
caso("C06-06", 6, "Fechas que cruzan el año", "PX", "4|Museo Cruce",
     "Día de más visitantes: 2027-01-01|Día de menos visitantes: 2026-12-30")

# ---------------------------------------------------------------- Días por nivel
caso("C07-01", 7, "Límites con aforo 500: 149, 150, 299, 300, 424 y 425", "PX", "4|Museo Niveles",
     "Días en asistencia baja: 1|Días en asistencia media: 2|Días en asistencia alta: 2|Días en asistencia plena: 1")
caso("C07-02", 7, "Límites con aforo 100: 29, 30, 59, 60, 84 y 85", "PX", "4|Museo Niveles Cien",
     "Días en asistencia baja: 1|Días en asistencia media: 2|Días en asistencia alta: 2|Días en asistencia plena: 1")
caso("C07-03", 7, "Museo del Mar: 2, 0, 2 y 1 (se muestra también el nivel con cero)", "PA", "4|Museo del Mar",
     "Días en asistencia baja: 2|Días en asistencia media: 0|Días en asistencia alta: 2|Días en asistencia plena: 1")
caso("C07-04", 7, "Casa de la Música: 1, 1, 1 y 1", "PA", "4|Casa de la Música",
     "Días en asistencia baja: 1|Días en asistencia media: 1|Días en asistencia alta: 1|Días en asistencia plena: 1")
caso("C07-05", 7, "Todos los días en asistencia plena (aforo completo)", "PX", "4|Museo Lleno",
     "Días en asistencia baja: 0|Días en asistencia media: 0|Días en asistencia alta: 0|Días en asistencia plena: 2")
caso("C07-06", 7, "Todos los días en asistencia baja", "PX", "4|Museo Bajo",
     "Días en asistencia baja: 3|Días en asistencia media: 0|Días en asistencia alta: 0|Días en asistencia plena: 0")

# ---------------------------------------------------------------- Racha en asistencia baja
caso("C08-01", 8, "Museo del Mar: 2 días desde 2026-11-02", "PA", "4|Museo del Mar",
     "Racha más larga en asistencia baja: 2 días (empezó el 2026-11-02)")
caso("C08-02", 8, "Dos rachas (2 y 3 días): gana la más larga", "PX", "4|Museo Rachas",
     "Racha más larga en asistencia baja: 3 días (empezó el 2026-11-04)")
caso("C08-03", 8, "Ningún día en asistencia baja", "PC1", "4|Museo del Café",
     "Racha más larga en asistencia baja: El museo no tuvo ningún día en asistencia baja.")
caso("C08-04", 8, "Dos rachas empatadas en 2 días: gana la primera", "PX", "4|Museo Rachas Iguales",
     "Racha más larga en asistencia baja: 2 días (empezó el 2026-11-01)")
caso("C08-05", 8, "Todos los días en asistencia baja", "PX", "4|Museo Bajo",
     "Racha más larga en asistencia baja: 3 días (empezó el 2026-11-01)")
caso("C08-06", 8, "Racha de un solo día", "PA", "4|Casa de la Música",
     "Racha más larga en asistencia baja: 1 día (empezó el 2026-11-01)")
caso("C08-07", 8, "La racha termina en el último día registrado", "PX", "4|Museo Racha Final",
     "Racha más larga en asistencia baja: 2 días (empezó el 2026-11-02)")
caso("C08-08", 8, "La racha más larga es la primera y hay otra corta después", "PX", "4|Museo Racha Primero",
     "Racha más larga en asistencia baja: 3 días (empezó el 2026-11-01)")

# ---------------------------------------------------------------- Días sin registrar
caso("C09-01", 9, "Museo del Mar: último día 2026-11-05 y los días que faltan hasta ayer", "PA",
     "4|Museo del Mar", "Último día registrado: 2026-11-05|Días sin registrar: {FALT_MAR}")
caso("C09-02", 9, "Museo con registro muy atrasado (último día 2020-01-03)", "PX", "4|Museo Pasado",
     "Último día registrado: 2020-01-03|Días sin registrar: {FALT_PASADO}")
caso("C09-03", 9, "Registro en el futuro (último día en 2100): está al día", "PX", "4|Museo Futuro",
     "Último día registrado: 2100-01-03|Días sin registrar: El registro está al día.")
caso("C09-04", 9, "Último día registrado igual a ayer: está al día", "P0",
     "1|Museo Reciente|100|{AYER_A}|{AYER_M}|{AYER_D}|2|Museo Reciente|10|4|Museo Reciente",
     "Último día registrado: {AYER}|Días sin registrar: El registro está al día.")
caso("C09-05", 9, "Último día registrado igual a anteayer: falta 1 día", "P0",
     "1|Museo Reciente|100|{ANTE_A}|{ANTE_M}|{ANTE_D}|2|Museo Reciente|10|4|Museo Reciente",
     "Último día registrado: {ANTE}|Días sin registrar: Faltan 1 día (del {AYER} al {AYER}).")
caso("C09-06", 9, "Último día registrado igual a hoy: está al día", "P0",
     "1|Museo Reciente|100|{HOY_A}|{HOY_M}|{HOY_D}|2|Museo Reciente|10|4|Museo Reciente",
     "Último día registrado: {HOY}|Días sin registrar: El registro está al día.")
caso("C09-07", 9, "Días simulados que pasan de hoy: está al día", "P0",
     "1|Museo Reciente|100|{HOY_A}|{HOY_M}|{HOY_D}|3|Museo Reciente|3|10|20|4|Museo Reciente",
     "Días registrados: 3|Días sin registrar: El registro está al día.")
caso("C09-08", 9, "Museo con un día registrado el 2026-11-01 (según la fecha del computador)",
     "PC1", "4|Museo del Café",
     "Último día registrado: 2026-11-01|Días sin registrar: {FALT_CAFE}")

# ---------------------------------------------------------------- Varios museos
caso("C10-01", 10, "Cuatro museos: cada informe muestra sus propios datos", "PR",
     "4|Museo del Mar|4|Casa de la Música|4|Museo del Café|4|Galería del Puerto",
     "Museo: Museo del Mar|Aforo diario: 500|Visitantes totales: 1420|"
     "Museo: Casa de la Música|Aforo diario: 200|Visitantes totales: 440|"
     "Museo: Museo del Café|Aforo diario: 150|Visitantes totales: 60|"
     "Museo: Galería del Puerto|Aforo diario: 100|" + SIN_DIAS)
caso("C10-02", 10, "Museo del Banano no existe", "PR", "4|Museo del Banano", NO_HAY)
caso("C10-03", 10, "museo del mar en minúsculas no existe", "PR", "4|museo del mar", NO_HAY)
caso("C10-04", 10, "Museo del Cafe sin tilde no existe", "PR", "4|Museo del Cafe", NO_HAY)
caso("C10-05", 10, "Nombre con espacios al inicio y al final sí existe", "PR", "4| Museo del Mar |",
     "Museo: Museo del Mar|Visitantes totales: 1420")
caso("C10-06", 10, "Museos creados por teclado conviven y no se mezclan los días", "P0",
     "1|Museo Uno|100|2026|11|1|1|Museo Dos|200|2026|11|1|2|Museo Uno|40|4|Museo Dos|4|Museo Uno",
     "Museo: Museo Dos|" + SIN_DIAS + "|Museo: Museo Uno|Visitantes totales: 40")
caso("C10-07", 10, "Sin ningún museo, el informe avisa", "P0", "4|Museo del Mar", NO_HAY)

# ---------------------------------------------------------------- Porcentaje más alto y más bajo
caso("C11-01", 11, "Mar 56.8 %, Casa 55.0 %, Café 40.0 % y Galería sin días", "PR", "5",
     "Mayor porcentaje de asistencia: Museo del Mar, 56.8 %|"
     "Menor porcentaje de asistencia: Museo del Café, 40.0 %", ausente="Galería del Puerto")
caso("C11-02", 11, "Sin ningún museo", "P0", "5", "Ningún museo tiene días registrados.")
caso("C11-03", 11, "Con un museo sin días registrados", "P0",
     "1|Galería del Puerto|100|2026|11|1|5", "Ningún museo tiene días registrados.",
     ausente="Mayor porcentaje")
caso("C11-04", 11, "Un solo museo con días: es el más alto y el más bajo", "PC1", "5",
     "Mayor porcentaje de asistencia: Museo del Café, 40.0 %|"
     "Menor porcentaje de asistencia: Museo del Café, 40.0 %")
caso("C11-05", 11, "Un museo sin días no cuenta como 0 %, aunque se cree primero", "P0",
     "1|Galería del Puerto|100|2026|11|1|1|Museo del Café|150|2026|11|1|2|Museo del Café|60|5",
     "Mayor porcentaje de asistencia: Museo del Café, 40.0 %|"
     "Menor porcentaje de asistencia: Museo del Café, 40.0 %", ausente="Galería del Puerto")
caso("C11-06", 11, "Empate exacto (50 % y 50 %): cuenta el que se creó primero", "PEX", "5",
     "Mayor porcentaje de asistencia: Museo Uno, 50.0 %|Menor porcentaje de asistencia: Museo Uno, 50.0 %")
caso("C11-07", 11, "Empate que la aritmética decimal no ve igual (16.67 %): gana el primero", "PED", "5",
     "Mayor porcentaje de asistencia: Museo Seis, 16.67 %|Menor porcentaje de asistencia: Museo Seis, 16.67 %")
caso("C11-08", 11, "El mismo empate con el orden de creación invertido: gana Museo Tres", "PEDI", "5",
     "Mayor porcentaje de asistencia: Museo Tres, 16.67 %|Menor porcentaje de asistencia: Museo Tres, 16.67 %")
caso("C11-09", 11, "Se compara sin redondear: 33.333 % supera a 33.33 % aunque se muestran igual", "PSR", "5",
     "Mayor porcentaje de asistencia: Museo Tres Plazas, 33.33 %|"
     "Menor porcentaje de asistencia: Museo Diez Mil, 33.33 %")

# ---------------------------------------------------------------- Cargar los museos
caso("C12-01", 12, "Archivo de museos del enunciado: 2 museos y 5 líneas descartadas", "P0",
     "6|museos.csv|museos_sin_datos.csv",
     "Línea 4 descartada: El aforo diario debe ser de al menos un visitante.|"
     "Línea 5 descartada: No tiene cinco campos.|"
     "Línea 6 descartada: El aforo diario debe ser un número entero.|"
     "Línea 7 descartada: Ya existe un museo con ese nombre.|"
     "Línea 8 descartada: La fecha no es válida.|Se cargaron 2 museos.")
caso("C12-02", 12, "Orden de las causas y número de línea (con líneas vacías y de espacios)", "P0",
     "6|museos_pruebas.csv|museos_sin_datos.csv",
     "Línea 4 descartada: No tiene cinco campos.|Línea 5 descartada: No tiene cinco campos.|"
     "Línea 6 descartada: El nombre no puede estar vacío.|Línea 7 descartada: El nombre no puede estar vacío.|"
     "Línea 8 descartada: Ya existe un museo con ese nombre.|"
     "Línea 9 descartada: Ya existe un museo con ese nombre.|"
     "Línea 10 descartada: El aforo diario debe ser un número entero.|"
     "Línea 11 descartada: El aforo diario debe ser de al menos un visitante.|"
     "Línea 12 descartada: El aforo diario debe ser de al menos un visitante.|"
     "Línea 13 descartada: El aforo diario debe ser un número entero.|"
     "Línea 14 descartada: El aforo diario debe ser un número entero.|"
     "Línea 15 descartada: La fecha no es válida.|Línea 16 descartada: La fecha no es válida.|"
     "Línea 17 descartada: La fecha no es válida.|Línea 18 descartada: La fecha no es válida.|"
     "Línea 21 descartada: El nombre no puede estar vacío.|Se cargaron 22 museos.",
     ausente="Línea 2 descartada|Línea 3 descartada|Línea 19 descartada|Línea 20 descartada|"
             "Línea 22 descartada|Línea 23 descartada|Línea 24 descartada|Línea 25 descartada|"
             "Línea 26 descartada|Línea 27 descartada|Línea 28 descartada")
caso("C12-03", 12, "Espacios alrededor de los campos: los museos se crean con el nombre limpio", "P0",
     "6|museos_pruebas.csv|museos_sin_datos.csv|4|Museo Uno|4|Museo Dos|4|Museo Tres",
     "Se cargaron 22 museos.|Museo: Museo Uno|Aforo diario: 100|Museo: Museo Dos|Aforo diario: 200|"
     "Museo: Museo Tres|Aforo diario: 300")
caso("C12-04", 12, "Fecha bisiesta (2028) y aforo mínimo (1) se cargan bien", "P0",
     "6|museos_pruebas.csv|museos_sin_datos.csv|4|Museo M|4|Museo N",
     "Museo: Museo M|Aforo diario: 100|Museo: Museo N|Aforo diario: 1")
caso("C12-05", 12, "Archivo de museos inexistente: no lee la ruta de visitantes", "P0",
     "6|no_existe.csv|museos.csv|4|Museo del Mar",
     "El archivo no existe.|" + NO_HAY, ausente="Se cargaron", veces={INVALIDA: 1})
caso("C12-06", 12, "Archivo con solo el encabezado: el ciclo no hace ninguna iteración", "P0",
     "6|museos_sin_datos.csv|museos_sin_datos.csv",
     "Se cargaron 0 museos.|Se cargaron 0 días.", ausente="descartada")
caso("C12-07", 12, "Con un museo creado por teclado: avisa y no lee ninguna ruta", "PC",
     "6|museos.csv|visitantes.csv", "La carga solo se hace con el programa sin museos.",
     ausente="Se cargaron", veces={INVALIDA: 2})
caso("C12-08", 12, "Una segunda carga no agrega otra vez los días", "PA",
     "6|museos.csv|visitantes.csv|4|Museo del Mar",
     "La carga solo se hace con el programa sin museos.|Días registrados: 5|Visitantes totales: 1420",
     ausente="Se cargaron", veces={INVALIDA: 2})
caso("C12-09", 12, "Un museo cargado no puede crearse otra vez por teclado", "PA",
     "1|Museo del Mar|300|2026|11|1", "Ya existe un museo con ese nombre.", ausente=NO_CREADO)
caso("C12-10", 12, "Archivo de museos que no está en UTF-8 (exportado de Excel como ANSI)", "P0",
     "6|museos_ansi.csv|visitantes.csv|4|Museo del Mar",
     NO_UTF8 + "|" + NO_HAY, ausente="Se cargaron", veces={INVALIDA: 1})
caso("C12-11", 12, "La ruta es una carpeta y no un archivo", "P0",
     "6|.|visitantes.csv",
     "El archivo no existe.", ausente="Se cargaron", veces={INVALIDA: 1})
caso("C12-12", 12, "Ruta con espacios al inicio y al final", "P0",
     "6|  museos.csv  |museos_sin_datos.csv", "Se cargaron 2 museos.", ausente="El archivo no existe.")

# ---------------------------------------------------------------- Cargar los visitantes
caso("C13-01", 13, "Archivos del enunciado: 9 días y 5 líneas descartadas", "P0",
     "6|museos.csv|visitantes.csv|4|Museo del Mar|4|Casa de la Música",
     "Se cargaron 2 museos.|Línea 10 descartada: Los visitantes van de 0 a 200.|"
     "Línea 12 descartada: No hay un museo con ese nombre.|"
     "Línea 13 descartada: Los visitantes van de 0 a 500.|"
     "Línea 14 descartada: Los visitantes deben ser un número entero.|"
     "Línea 15 descartada: No tiene dos campos.|Se cargaron 9 días.|"
     "Visitantes totales: 1420|Visitantes totales: 440|Último día registrado: 2026-11-04")
caso("C13-02", 13, "Orden de las causas, límites 0 y aforo, y espacios en los campos", "P0",
     "6|museos_pruebas.csv|visitantes_pruebas.csv|4|Museo del Mar|4|Casa de la Música",
     "Línea 3 descartada: No tiene dos campos.|Línea 4 descartada: No tiene dos campos.|"
     "Línea 5 descartada: No hay un museo con ese nombre.|Línea 6 descartada: No hay un museo con ese nombre.|"
     "Línea 7 descartada: Los visitantes deben ser un número entero.|"
     "Línea 8 descartada: Los visitantes deben ser un número entero.|"
     "Línea 9 descartada: Los visitantes van de 0 a 500.|Línea 10 descartada: Los visitantes van de 0 a 500.|"
     "Línea 16 descartada: Los visitantes van de 0 a 200.|Línea 17 descartada: No hay un museo con ese nombre.|"
     "Línea 18 descartada: Los visitantes deben ser un número entero.|"
     "Línea 20 descartada: " + LIMITE + "|Se cargaron 63 días.|"
     "Días registrados: 4|Visitantes totales: 1020|Porcentaje de asistencia: 51.0 %|"
     "Días registrados: 1|Visitantes totales: 200|Porcentaje de asistencia: 100.0 %")
caso("C13-03", 13, "Archivo de visitantes inexistente: los museos quedan cargados sin días", "P0",
     "6|museos.csv|no_existe.csv|4|Museo del Mar",
     "Se cargaron 2 museos.|El archivo no existe.|" + SIN_DIAS,
     ausente="Se cargaron 0|Días registrados:")
caso("C13-04", 13, "Archivo de visitantes que no está en UTF-8: los museos quedan sin días", "P0",
     "6|museos.csv|museos_ansi.csv|4|Museo del Mar",
     "Se cargaron 2 museos.|" + NO_UTF8 + "|" + SIN_DIAS, ausente="Días registrados:")
caso("C13-05", 13, "Sin museos cargados, todas las líneas se descartan", "P0",
     "6|museos_sin_datos.csv|visitantes.csv",
     "Se cargaron 0 museos.|Línea 2 descartada: No hay un museo con ese nombre.|"
     "Línea 15 descartada: No tiene dos campos.|Se cargaron 0 días.")
caso("C13-06", 13, "Una línea descartada no consume un día: la Casa queda con 4 días seguidos", "PA",
     "4|Casa de la Música",
     "Días registrados: 4|Visitantes totales: 440|Último día registrado: 2026-11-04")
caso("C13-07", 13, "Un archivo de museos usado como archivo de visitantes: cada línea tiene cinco campos", "P0",
     "6|museos.csv|museos.csv",
     "Se cargaron 2 museos.|Línea 2 descartada: No tiene dos campos.|"
     "Línea 8 descartada: No tiene dos campos.|Se cargaron 0 días.")

# ---------------------------------------------------------------- El menú
caso("C14-01", 14, "El menú muestra las siete opciones en orden y 7 termina el programa", "P0", "7",
     "1. Crear museo|2. Registrar visitantes del día siguiente|3. Simular días|4. Informe de museo|"
     "5. Museo con mayor y menor porcentaje de asistencia|6. Cargar museos y visitantes desde archivos|"
     "7. Salir|Hasta luego.", menus=1)
caso("C14-02", 14, "Opción 8: avisa y vuelve a mostrar el menú", "P0", "8", INVALIDA, menus=2)
caso("C14-03", 14, "Opción escrita como dos: avisa y vuelve a mostrar el menú", "P0", "dos", INVALIDA, menus=2)
caso("C14-04", 14, "Opción vacía (solo Enter)", "P0", "<ENTER>", INVALIDA, menus=2)
caso("C14-05", 14, "Otras opciones inexistentes: 0, 71 y -1", "P0", "0|71|-1", INVALIDA,
     veces={INVALIDA: 3}, menus=4)
caso("C14-06", 14, "Después de crear, registrar y ver un informe, el menú vuelve a mostrarse", "P0",
     "1|Museo del Café|150|2026|11|1|2|Museo del Café|60|4|Museo del Café",
     "Museo creado, sin días registrados.|Día registrado.|Museo: Museo del Café", menus=4)
caso("C14-07", 14, "Con 7 el programa termina y no atiende lo que se teclee después", "P0",
     "7|1|Museo A", "Hasta luego.", ausente="--- Crear museo ---", menus=1)
caso("C14-08", 14, "Después de cada opción distinta de salir vuelve el menú (5 y 6 incluidas)", "P0",
     "5|6|museos_sin_datos.csv|museos_sin_datos.csv|3|Museo A",
     "Ningún museo tiene días registrados.|Se cargaron 0 museos.|" + NO_HAY, menus=4)
caso("C14-09", 14, "Opción con espacios alrededor ( 7 ): se acepta", "P0", " 7 ", "Hasta luego.", menus=1)

# ---------------------------------------------------------------- Límite del calendario
caso("C15-01", 15, "Desde 9999-12-30 caben dos días, el tercero se rechaza", "PL",
     "2|Fin|1|2|Fin|1|2|Fin",
     "Día a registrar: 9999-12-30|Día registrado.|Día a registrar: 9999-12-31|Día registrado.|" + LIMITE,
     veces={"Día registrado.": 2})
caso("C15-02", 15, "Simular 3 días desde 9999-12-30: se rechaza y no se agrega ninguno", "PL",
     "3|Fin|3|1|5|4|Fin",
     LIMITE + "|" + SIN_DIAS, ausente="Se simularon")
caso("C15-03", 15, "Simular 2 días desde 9999-12-30: caben justo", "PL",
     "3|Fin|2|1|5|4|Fin",
     "Se simularon 2 días para Fin.|Días registrados: 2|Último día registrado: 9999-12-31")
caso("C15-04", 15, "Simular un billón de días: se rechaza al instante", "PL",
     "3|Fin|1000000000000|1|5|4|Fin",
     LIMITE + "|" + SIN_DIAS, ausente="Se simularon")
caso("C15-05", 15, "Simular 1 día y luego registrar otro desde 9999-12-30", "PL",
     "3|Fin|1|1|5|2|Fin|3|4|Fin",
     "Se simularon 1 días para Fin.|Día a registrar: 9999-12-31|Día registrado.|"
     "Días registrados: 2|Último día registrado: 9999-12-31")
caso("C15-06", 15, "Carga de archivos: la línea que no cabe se descarta con su causa", "P0",
     "6|museos_pruebas.csv|visitantes_pruebas.csv|4|Fin",
     "Línea 20 descartada: " + LIMITE + "|Se cargaron 63 días.|"
     "Días registrados: 1|Último día registrado: 9999-12-31")
