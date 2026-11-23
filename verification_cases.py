#Comprueba los casos de verificación ejecutando user_interface.py.
import os
import re
import subprocess
import sys
from datetime import date, timedelta

from casos import CASOS, PREP

CARPETA = os.path.dirname(os.path.abspath(__file__))
PROGRAMA = os.path.join(CARPETA, "user_interface.py")
TITULO_MENU = "Programa de registro de museos"


# Valores de hoy, ayer y anteayer, y textos de días faltantes.
def marcas_de_fecha() -> dict:
    """Valores que dependen de la fecha del computador (requisito 9)."""
    hoy = date.today()
    ayer = hoy - timedelta(days=1)
    marcas = {}
    for nombre, fecha in (("HOY", hoy), ("AYER", ayer), ("ANTE", hoy - timedelta(days=2))):
        marcas[nombre] = str(fecha)
        marcas[nombre + "_A"] = str(fecha.year)
        marcas[nombre + "_M"] = str(fecha.month)
        marcas[nombre + "_D"] = str(fecha.day)

    def faltantes(ultimo: date) -> str:
        if ultimo >= ayer:
            return "El registro está al día."
        cantidad = (ayer - ultimo).days
        palabra = "día" if cantidad == 1 else "días"
        return f"Faltan {cantidad} {palabra} (del {ultimo + timedelta(days=1)} al {ayer})."

    marcas["FALT_MAR"] = faltantes(date(2026, 11, 5))
    marcas["FALT_PASADO"] = faltantes(date(2020, 1, 3))
    marcas["FALT_CAFE"] = faltantes(date(2026, 11, 1))
    return marcas


# Corre user_interface.py con las entradas y devuelve su salida y sus errores.
def ejecutar(entradas: list) -> tuple:
    entorno = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    try:
        r = subprocess.run([sys.executable, PROGRAMA], input="\n".join(entradas) + "\n",
                           capture_output=True, text=True, encoding="utf-8",
                           cwd=CARPETA, env=entorno, timeout=60)
    except subprocess.TimeoutExpired:
        return "", "El programa no terminó en 60 segundos (se quedó repitiendo o esperando)."
    return r.stdout, r.stderr


# Ejecuta un caso y devuelve la lista de fallos y la salida del caso.
def verificar(caso: dict, marcas: dict) -> tuple:
    pasos = PREP[caso["prep"]][1]
    entradas_prep = [x for paso in pasos for x in paso]
    entradas = [x.format(**marcas) for x in caso["entradas"]]
    esperado = [x.format(**marcas) for x in caso["esperado"]]
    ausente = [x.format(**marcas) for x in caso["ausente"]]

    todas = entradas_prep + entradas
    if not (entradas and entradas[0].strip() == "7"):
        todas = todas + ["7"]

    salida, errores = ejecutar(todas)
    trozos = salida.split(TITULO_MENU)
    propia = "".join(trozos[len(pasos) + 1:])    # solo lo que se ve después de la preparación
    fallos = []

    if errores.strip():
        fallos.append("el programa terminó con un error:\n" + errores.strip()[-600:])

    posicion = 0
    for linea in esperado:
        i = propia.find(linea, posicion)
        if i < 0:
            fallos.append(f"no aparece (o aparece fuera de orden): «{linea}»")
        else:
            posicion = i + len(linea)

    for linea in ausente:
        if linea in propia:
            fallos.append(f"no debía aparecer: «{linea}»")

    for linea, n in caso["veces"].items():
        real = propia.count(linea)
        if real != n:
            fallos.append(f"«{linea}» debía aparecer {n} vez/veces y apareció {real}")

    if caso["total_en"]:
        bajo, alto = caso["total_en"]
        totales = [int(x) for x in re.findall(r"Visitantes totales: (\d+)", propia)]
        if not totales or not (bajo <= totales[-1] <= alto):
            fallos.append(f"Visitantes totales debía estar entre {bajo} y {alto}; fue {totales[-1:] or 'ninguno'}")

    if caso["menus"] is not None:
        real = len(trozos) - 1 - len(pasos)
        if real != caso["menus"]:
            fallos.append(f"el menú debía mostrarse {caso['menus']} vez/veces y se mostró {real}")

    return fallos, propia


# Corre los casos pedidos (o todos) y muestra el resultado.
def main():
    argumentos = sys.argv[1:]
    detalle = "--detalle" in argumentos
    ids = [a for a in argumentos if a != "--detalle"]
    if not os.path.exists(PROGRAMA):
        print(f"No se encontró {os.path.abspath(PROGRAMA)}")
        sys.exit(1)

    marcas = marcas_de_fecha()
    casos = [c for c in CASOS if not ids or c["id"] in ids]
    falladas = []
    for caso in casos:
        fallos, propia = verificar(caso, marcas)
        print(f"{'OK   ' if not fallos else 'FALLA'} {caso['id']}  {caso['titulo']}")
        for fallo in fallos:
            print("        -", fallo)
        if fallos:
            falladas.append(caso["id"])
        if detalle:
            for linea in propia.splitlines():
                if linea.strip():
                    print("        |", linea)

    print(f"\n{len(casos) - len(falladas)} de {len(casos)} casos pasaron.")
    if falladas:
        print("Fallaron:", ", ".join(falladas))
    sys.exit(0 if not falladas else 1)


if __name__ == "__main__":
    main()
