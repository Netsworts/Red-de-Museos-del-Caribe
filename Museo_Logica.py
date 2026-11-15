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

 


         

 
