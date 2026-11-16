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
     
    def simular_dias(self, dias, minimo, maximo):
        for d in range(dias):
            self.registrar_dia(random.randint(minimo, maximo))
    
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





 


         

 
