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
        
    # --- Día de más y día de menos visitantes ---
    def indice_extremo(self, buscar_el_mayor: bool) -> int:
        # Con > y < estrictos, en un empate se queda el primer día.
        indice_elegido = 0
        for indice in range(1, len(self.visitantes)):
            if buscar_el_mayor:
                if self.visitantes[indice] > self.visitantes[indice_elegido]:
                    indice_elegido = indice
            else:
                if self.visitantes[indice] < self.visitantes[indice_elegido]:
                    indice_elegido = indice
        return indice_elegido

    # Fecha del día con más visitantes.
    def fecha_con_mas_visitantes(self) -> date:
        return self.fecha_dia(self.indice_extremo(True))

    # Fecha del día con menos visitantes.
    def fecha_con_menos_visitantes(self) -> date:
        return self.fecha_dia(self.indice_extremo(False))

   # --- Días en cada nivel de asistencia ---
    def nivel_asistencia_dia(self, visitantes: int) -> str:
        LIMITE_BAJA = 30     # porcentajes del aforo, según la tabla del enunciado
        LIMITE_MEDIA = 60
        LIMITE_ALTA = 85
        # Se multiplica en lugar de dividir para comparar enteros exactos.
        if visitantes * 100 < LIMITE_BAJA * self.aforo_diario:
            return "baja"
        elif visitantes * 100 < LIMITE_MEDIA * self.aforo_diario:
            return "media"
        elif visitantes * 100 < LIMITE_ALTA * self.aforo_diario:
            return "alta"
        else:
            return "plena"

    # Cuántos días hay en cada nivel.
    def dias_por_nivel(self) -> dict:
        dias = {"baja": 0, "media": 0, "alta": 0, "plena": 0}
        for visitantes in self.visitantes:
            nivel = self.nivel_asistencia_dia(visitantes)
            dias[nivel] = dias[nivel] + 1
        return dias

    # --- Racha más larga en asistencia baja ---
    def racha_asistencia_baja(self) -> dict:
        mejor = {"dias": 0, "inicio": None}
        dias_actuales = 0
        inicio_actual = None
        for indice in range(len(self.visitantes)):
            if self.nivel_asistencia_dia(self.visitantes[indice]) == "baja":
                if dias_actuales == 0:
                    inicio_actual = self.fecha_dia(indice)
                dias_actuales = dias_actuales + 1
                if dias_actuales > mejor["dias"]:    # > deja la primera racha si empatan
                    mejor["dias"] = dias_actuales
                    mejor["inicio"] = inicio_actual
            else:
                dias_actuales = 0
        return mejor

        # --- Días sin registrar ---
    def dias_sin_registrar(self, fecha_actual: date) -> int:
        ayer = fecha_actual - timedelta(days=1)
        ultima = self.ultima_fecha_registrada()
        if ultima >= ayer:
            return 0
        return (ayer - ultima).days

    # --- Informe de un museo ---
    def generar_informe(self, fecha_actual: date) -> str:
        informe = f"Museo: {self.nombre}\n"
        informe = informe + f"Aforo diario: {self.aforo_diario}\n"
        if len(self.visitantes) == 0:
            return informe + "El museo no tiene días registrados."

        informe = informe + f"Días registrados: {len(self.visitantes)}\n"
        informe = informe + f"Visitantes totales: {self.total_visitantes()}\n"
        informe = informe + f"Promedio de visitantes por día: {round(self.promedio_visitantes(), 2)}\n"
        informe = informe + f"Porcentaje de asistencia: {round(self.porcentaje_asistencia(), 2)} %\n"
        informe = informe + f"Desviación estándar: {round(self.desviacion_estandar(), 2)}\n"
        informe = informe + f"Día de más visitantes: {self.fecha_con_mas_visitantes()}\n"
        informe = informe + f"Día de menos visitantes: {self.fecha_con_menos_visitantes()}\n"
        
        dias = self.dias_por_nivel()
        for nivel in dias:
            informe = informe + f"Días en asistencia {nivel}: {dias[nivel]}\n"

        racha = self.racha_asistencia_baja()
        if racha["inicio"] is None:
            texto_racha = "El museo no tuvo ningún día en asistencia baja."
        else:
            texto_racha = f"{dias_en_texto(racha['dias'])} (empezó el {racha['inicio']})"
 
        informe = informe + f"Racha más larga en asistencia baja: {texto_racha}\n"

        informe = informe + f"Último día registrado: {self.ultima_fecha_registrada()}\n"
        faltan = self.dias_sin_registrar(fecha_actual)
        if faltan == 0:
            texto_faltantes = "El registro está al día."
        else:
            desde = self.ultima_fecha_registrada() + timedelta(days=1)
            hasta = fecha_actual - timedelta(days=1)
            texto_faltantes = f"Faltan {dias_en_texto(faltan)} (del {desde} al {hasta})."
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

    



      



 


         

 
