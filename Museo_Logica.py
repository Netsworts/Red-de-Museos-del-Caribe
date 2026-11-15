from datetime import date, timedelta


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
         

 
