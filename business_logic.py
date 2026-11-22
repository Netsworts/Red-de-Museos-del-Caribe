from datetime import date, timedelta
from random import randint

# Un museo: sus datos y la lista de visitantes por día.
class Museo:
    # Guarda nombre, aforo, fecha de inicio y una lista vacía de visitantes.
    def __init__(self, nombre, aforo_diario, fecha_inicio):
        self.nombre = nombre
        self.aforo_diario = aforo_diario
        self.fecha_inicio = fecha_inicio
        self.visitantes = []

    # --- Registrar el día siguiente ---
    def registrar_dia(self, visitantes: int):
        self.visitantes.append(visitantes)

    # Fecha del próximo día que se puede registrar.
    def fecha_siguiente(self) -> date:
        return self.fecha_inicio + timedelta(days=len(self.visitantes))

    # Convierte el texto a entero y revisa que esté entre 0 y el aforo.
    def validar_visitantes(self, texto: str) -> int:
        try:
            visitantes = int(texto)
        except ValueError:
            raise ValueError("Los visitantes deben ser un número entero.")
        if visitantes < 0 or visitantes > self.aforo_diario:
            raise ValueError(f"Los visitantes van de 0 a {self.aforo_diario}.")
        return visitantes
    
    # --- Simular días ---
    def validar_num_dias(self, texto: str) -> int:
        try:
            dias = int(texto)
        except ValueError:
            raise ValueError("El número de días debe ser un número entero.")
        if dias < 1:
            raise ValueError("Se debe simular al menos un día.")
        return dias

    # Revisa que el mínimo no sea mayor que el máximo.
    def validar_rango(self, minimo: int, maximo: int):
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")
    
    # Agrega días con visitantes al azar entre el mínimo y el máximo.
    def simular_dias(self, dias: int, minimo: int, maximo: int):
        for d in range(dias):
            self.registrar_dia(random.randint(minimo, maximo))
    
    # --- Fechas: el índice 0 es la fecha de inicio ---
    def fecha_dia(self, indice: int) -> date:
        return self.fecha_inicio + timedelta(days=indice)

    # --- Total, promedio, porcentaje y desviación ---
    # Desde aquí, los métodos suponen al menos un día registrado.
    def total_visitantes(self) -> int:
        total = 0
        for visitantes in self.visitantes:
            total = total + visitantes
        return total

    # Total de visitantes dividido entre los días.
    def promedio_visitantes(self) -> float:
        return self.total_visitantes() / len(self.visitantes)

    # Total de visitantes como porcentaje del aforo de todos los días.
    def porcentaje_asistencia(self) -> float:
        # Una sola división: así los empates dan exactamente el mismo número.
        return self.total_visitantes() * 100 / (len(self.visitantes) * self.aforo_diario)

    # Desviación estándar de los visitantes por día.
    def desviacion_estandar(self) -> float:
        promedio = self.promedio_visitantes()
        suma_cuadrados = 0
        for visitantes in self.visitantes:
            suma_cuadrados = suma_cuadrados + (visitantes - promedio) ** 2
        return (suma_cuadrados / len(self.visitantes)) ** 0.5

    def obtener_dias_extremos(self):
        indice_max = 0
        indice_min = 0

        for i in range(1, len(self.visitantes)):
            if self.visitantes[i] > self.visitantes[indice_max]:
                indice_max = i
            if self.visitantes[i] < self.visitantes[indice_min]:
                indice_min = i

        fecha_max = self.fecha_inicio + timedelta(days=indice_max)
        fecha_min = self.fecha_inicio + timedelta(days=indice_min)
        return fecha_max, fecha_min

    def clasificar_asistencia(self, visitantes_dia):
        porcentaje_dia = visitantes_dia / self.aforo_diario * 100
        if porcentaje_dia < 30:
            return "Baja"
        elif porcentaje_dia < 60:
            return "Media"
        elif porcentaje_dia < 85:
            return "Alta"
        else:
            return "Plena"

    def contar_dias_por_nivel(self):
        niveles = {
            "Baja": 0,
            "Media": 0,
            "Alta": 0,
            "Plena": 0,
        }
        for visitantes in self.visitantes:
            nivel = self.clasificar_asistencia(visitantes)
            niveles[nivel] += 1
        return niveles

    def obtener_racha_baja(self):
        racha_actual = 0
        inicio_actual = None
        max_racha = 0
        inicio_max = None

        for i in range(len(self.visitantes)):
            if self.clasificar_asistencia(self.visitantes[i]) == "Baja":
                if racha_actual == 0:
                    inicio_actual = self.fecha_inicio + timedelta(days=i)
                racha_actual += 1
                if racha_actual > max_racha:
                    max_racha = racha_actual
                    inicio_max = inicio_actual
            else:
                racha_actual = 0
                inicio_actual = None

        return max_racha, inicio_max

    def calcular_dias_sin_registrar(self, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = date.today()

        ultimo_dia = self.fecha_inicio + timedelta(days=len(self.visitantes) - 1)
        ayer = fecha_actual - timedelta(days=1)

        if ultimo_dia >= ayer:
            return ultimo_dia, True, 0, None, None

        dias_faltantes = (ayer - ultimo_dia).days
        desde = ultimo_dia + timedelta(days=1)
        return ultimo_dia, False, dias_faltantes, desde, ayer
    
    # --- Informe de un museo ---
    def generar_informe(self) -> str:
        informe = f"Museo: {self.nombre}\n"
        informe = informe + f"Aforo diario: {self.aforo_diario}\n"
        if len(self.visitantes) == 0:
            return informe + "El museo no tiene días registrados."

        informe = informe + f"Días registrados: {len(self.visitantes)}\n"
        informe = informe + f"Visitantes totales: {self.total_visitantes()}\n"
        informe = informe + f"Promedio de visitantes por día: {round(self.promedio_visitantes(), 2)}\n"
        informe = informe + f"Porcentaje de asistencia: {round(self.porcentaje_asistencia(), 2)} %\n"
        informe = informe + f"Desviación estándar: {round(self.desviacion_estandar(), 2)}\n"
        fecha_max, fecha_min = self.obtener_dias_extremos()
        informe = informe + f"Día de más visitantes: {fecha_max}\n"
        informe = informe + f"Día de menos visitantes: {fecha_min}\n"

        niveles = self.contar_dias_por_nivel()
        informe = informe + f"Días en asistencia baja: {niveles['Baja']}\n"
        informe = informe + f"Días en asistencia media: {niveles['Media']}\n"
        informe = informe + f"Días en asistencia alta: {niveles['Alta']}\n"
        informe = informe + f"Días en asistencia plena: {niveles['Plena']}\n"

        max_racha, inicio_max = self.obtener_racha_baja()
        if max_racha == 0:
            texto_racha = "El museo no tuvo ningún día en asistencia baja."
        else:
            texto_racha = f"{dias_en_texto(max_racha)} (empezó el {inicio_max})"
        informe = informe + f"Racha más larga en asistencia baja: {texto_racha}\n"

        ultimo_dia, al_dia, dias_faltantes, desde, hasta = self.calcular_dias_sin_registrar()
        informe = informe + f"Último día registrado: {ultimo_dia}\n"
        if al_dia:
            texto_faltantes = "El registro está al día."
        else:
            texto_faltantes = f"Faltan {dias_en_texto(dias_faltantes)} (del {desde} al {hasta})."
        return informe + f"Días sin registrar: {texto_faltantes}"


# Escribe una cantidad de días: "1 día" o "N días".
def dias_en_texto(cantidad: int) -> str:
    if cantidad == 1:
        return "1 día"
    return f"{cantidad} días"


# --- Varios museos ---
def buscar_museo(nombre: str, museos: list) -> Museo:
    nombre = nombre.strip()
    for museo in museos:
        if museo.nombre == nombre:
            return museo
    raise ValueError("No hay un museo con ese nombre.")


# --- Crear un museo ---
def validar_nombre(nombre: str, nombres_existentes: list) -> str:
    nombre = nombre.strip()
    if nombre == "":
        raise ValueError("El nombre no puede estar vacío.")
    if nombre in nombres_existentes:
        raise ValueError("Ya existe un museo con ese nombre.")
    return nombre


# Convierte el aforo a entero y revisa que sea al menos 1.
def validar_aforo(texto: str) -> int:
    try:
        aforo = int(texto)
    except ValueError:
        raise ValueError("El aforo diario debe ser un número entero.")
    if aforo < 1:
        raise ValueError("El aforo diario debe ser de al menos un visitante.")
    return aforo


# Revisa que año, mes y día formen una fecha válida.
def validar_fecha(año: str, mes: str, dia: str) -> date:
    try:
        return date(int(año), int(mes), int(dia))
    except ValueError:
        raise ValueError("La fecha no es válida.")


# Crea un museo; si un dato falla, lanza el error del primero.
def crear_museo_validado(nombre: str, aforo_diario: str, año: str, mes: str,
                         dia: str, nombres_existentes: list) -> Museo:
    # Valida en orden: nombre, aforo y fecha.
    nombre = validar_nombre(nombre, nombres_existentes)
    aforo = validar_aforo(aforo_diario)
    fecha = validar_fecha(año, mes, dia)
    return Museo(nombre, aforo, fecha)

    



      



 


         

 
