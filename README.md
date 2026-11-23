# Red de Museos del Caribe

Programa de consola en Python que lleva el registro de visitantes de los museos de la Red de Museos del Caribe y calcula sus indicadores de asistencia: total, promedio, porcentaje, desviación estándar, días extremos, niveles de asistencia, racha en asistencia baja y días sin registrar. También compara museos entre sí y carga los datos desde archivos CSV.

Proyecto final de Fundamentos de Programación, Universidad del Magdalena. Alternativa E: Los visitantes de la Red de Museos del Caribe.

## Equipo

| Integrante | Responsabilidad principal |
|---|---|
| Andrés | Requisitos 1 a 5: crear un museo, registrar, simular, informe y desviación estándar. Requisito agregado 15: límite del calendario |
| Héctor | Requisitos 6 a 9: día de más y de menos visitantes, niveles de asistencia, racha en asistencia baja y días sin registrar |
| Rafael | Requisitos 10 a 14: varios museos, porcentajes extremos, carga de archivos y menú. Requisito agregado 16: aviso de archivo que no está en UTF-8 |

## Video

[Ver el video explicativo](https://youtu.be/1sRg0dvcUoo)

## Cómo ejecutarlo

Se necesita Python 3.10 o posterior. Desde la carpeta del repositorio:

```
python user_interface.py
```

El menú tiene siete opciones: crear un museo, registrar los visitantes del día siguiente, simular días, ver el informe de un museo, ver el museo con mayor y menor porcentaje de asistencia, cargar museos y visitantes desde archivos, y salir.

Para probar la carga de archivos, en la opción 6 escriba `museos.csv` y luego `visitantes.csv`.

## Casos de verificación

Los 147 casos están en `casos.py`. Para ejecutarlos todos, desde la carpeta del repositorio:

```
python verification_cases.py
```

Al final debe decir `147 de 147 casos pasaron.` También se puede ejecutar solo algunos casos (`python verification_cases.py C11-07 C02-02`) o ver lo que muestra el programa en cada uno (`python verification_cases.py --detalle`). El documento `documentos/Casos_de_verificacion.docx` tiene cada caso con sus entradas, su salida esperada y su resultado.

## Contenido del repositorio

| Archivo o carpeta | Qué contiene |
|---|---|
| `business_logic.py` | La clase Museo y las funciones que validan, calculan y cargan archivos. No lee del teclado ni muestra nada |
| `user_interface.py` | El menú y la lectura de datos. Atrapa los errores y muestra sus mensajes |
| `casos.py` | Los 147 casos de verificación |
| `verification_cases.py` | El programa que ejecuta los casos sobre `user_interface.py` |
| `museos.csv`, `visitantes.csv` | Los archivos de ejemplo del enunciado |
| `museos_pruebas.csv`, `visitantes_pruebas.csv`, `museos_sin_datos.csv`, `museos_ansi.csv` | Los archivos de datos de los casos de verificación |
| `documentos/Documento_analisis.docx` | La especificación de cada requisito: entradas, salidas y reglas |
| `documentos/Informe_integral.docx` | Los incrementos, las decisiones de diseño, el diagrama de la clase, los algoritmos y la solución final |
| `documentos/Casos_de_verificacion.docx` | Los casos de verificación con su resultado |
| `documentos/Informe_IA.docx` | Cómo usó el equipo la inteligencia artificial, incremento por incremento |
| `evidencias_ia/` | Las conversaciones con la IA exportadas, que respaldan el informe de uso de la IA |

## Seguimiento del trabajo

- Cada incremento es un milestone con sus requisitos y su fecha prevista.
- Cada tarea es un issue asignado a quien la hizo y asociado a su incremento.
- El tablero del proyecto (pestaña Projects) muestra el estado de cada tarea.
- Las dificultades importantes están registradas como issues con la etiqueta `dificultad`, con la discusión y cómo se resolvieron.
