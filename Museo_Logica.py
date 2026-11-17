from datetime import date, timedelta
import random


class Museo:
    def __init__(self, nombre, aforo_diario, fecha_inicio):
        self.nombre = nombre
        self.aforo_diario = aforo_diario
        self.fecha_inicio = fecha_inicio
        self.visitantes = []

    def registrar_dia(self, visitantes):
        self.visitantes.append(visitantes)

    def fecha_siguiente(self):
        return self.fecha_inicio + timedelta(days=len(self.visitantes))
   
    def validar_visitantes(self, texto):
        try:
            visitantes = int(texto)
        except ValueError:
            raise ValueError("Los visitantes deben ser un número entero.")
        if visitantes < 0 or visitantes > self.aforo_diario:
            raise ValueError(f"Los visitantes van de 0 a {self.aforo_diario}.")
        return visitantes
    
    def validar_num_dias(self, texto):
        try:
            dias = int(texto)
        except ValueError:
            raise ValueError("El número de días debe ser un número entero.")
        if dias < 1:
            raise ValueError("Se debe simular al menos un día.")
        return dias
    
    def validar_rango(self, minimo, maximo):
        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo.")
     
    def simular_dias(self, dias, minimo, maximo):
        for d in range(dias):
            self.registrar_dia(random.randint(minimo, maximo))

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
    
    def generar_informe(self):
        if len(self.visitantes) == 0:
            return f"El museo {self.nombre} no tiene días registrados."

        dias_registrados = len(self.visitantes)
        total = sum(self.visitantes)
        promedio = total / dias_registrados
        porcentaje = promedio / self.aforo_diario * 100

        suma_cuadrados = 0
        for visitantes in self.visitantes:
            suma_cuadrados += (visitantes - promedio) ** 2
        desviacion_estandar = (suma_cuadrados / dias_registrados) ** 0.5

        return (
            f"Museo: {self.nombre}\n"
            f"Aforo diario: {self.aforo_diario}\n"
            f"Días registrados: {dias_registrados}\n"
            f"Visitantes totales: {total}\n"
            f"Promedio de visitantes por día: {round(promedio, 2)}\n"
            f"Porcentaje de ocupación: {round(porcentaje, 2)}%\n"
            f"Desviación estándar: {round(desviacion_estandar, 2)}"
        )


def buscar_museo(nombre, museos):
    nombre = nombre.strip()
    for museo in museos:
        if museo.nombre == nombre:
            return museo
    raise ValueError("No hay un museo con ese nombre.")


def validar_nombre(nombre, nombres_existentes):
    nombre = nombre.strip()
    if nombre == "":
        raise ValueError("El nombre no puede estar vacío.")
    if nombre in nombres_existentes:
        raise ValueError("Ya existe un museo con ese nombre.")
    return nombre


def validar_aforo(aforo_diario):
    try:
        aforo = int(aforo_diario)
    except ValueError:
        raise ValueError("El aforo diario debe ser un número entero.")
    if aforo < 1:
        raise ValueError("El aforo diario debe ser de al menos un visitante.")
    return aforo


def validar_fecha(año, mes, dia):
    try:
        return date(int(año), int(mes), int(dia))
    except ValueError:
        raise ValueError("La fecha no es válida.")
        

def crear_museo_validado(nombre, aforo_diario, año, mes,
                         dia, nombres_existentes):
    nombre = validar_nombre(nombre, nombres_existentes)
    aforo = validar_aforo(aforo_diario)
    fecha = validar_fecha(año, mes, dia)
    return Museo(nombre, aforo, fecha)
    



      



 


         

 
