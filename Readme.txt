MinExt-ADAII - Descripción Detallada de Archivos e Instrucciones de Ejecución

Archivos y Carpetas:

1. DatosProyecto/
   - Contiene archivos de datos originales en formato .txt.
   - Estos archivos representan las instancias iniciales del problema que serán procesadas.
   - Ejemplos incluyen Prueba1.txt, Prueba2.txt, hasta Prueba30.txt, y un archivo enunciado.txt con detalles del problema.

2. DatosDZN/
   - Contiene archivos en formato .dzn, que es el formato compatible con MiniZinc.
   - Estos archivos son generados automáticamente a partir de los datos en DatosProyecto mediante el script generar_datosDZN.py.
   - Ejemplos incluyen Prueba1.dzn, Prueba2.dzn, hasta Prueba30.dzn.

3. MisInstancias/
   - Carpeta para instancias personalizadas o adicionales para pruebas específicas.
   - Contiene archivos como Instancia1_Polarizada.txt, Instancia2_CostosAltos.txt, entre otros.

4. ProyectoGUIFuentes/
   - Contiene el código fuente de la interfaz gráfica del proyecto.
   - Incluye el archivo principal main.py que inicia la aplicación y utils.py con funciones auxiliares.

5. Proyecto.mzn
   - Archivo principal del modelo MiniZinc.
   - Define los parámetros de entrada, variables de decisión, restricciones y la función objetivo para minimizar el extremismo en la población.
   - Contiene la lógica completa del problema de optimización.

6. generar_datosDZN.py
   - Script en Python que convierte los archivos de DatosProyecto a formato .dzn.
   - Facilita la preparación de datos para ser usados por MiniZinc.

Instrucciones para ejecutar la aplicación:

1. Clonar el repositorio:
   git clone https://github.com/DiegoFernando01/MinExt-ADAII

2. Instalar las dependencias de Python (si no están instaladas):
   pip install -r requirements.txt

3. Convertir los datos al formato .dzn ejecutando:
   python generar_datosDZN.py

4. Ejecutar la interfaz gráfica con:
   python ProyectoGUIFuentes/main.py

Requisitos previos:
- Tener instalado Git.
- Tener Python 3.x instalado.
- Tener MiniZinc instalado y agregado al PATH del sistema.

8. ConvertirArchivos/
   - Contiene scripts y utilidades para la conversión y manejo de archivos.
   - Incluye:
     - README.md: Documentación específica de esta carpeta.
     - interfaz.py: Código para la interfaz relacionada con la conversión.
     - utils.py: Funciones auxiliares para la conversión y procesamiento de archivos.

Este archivo proporciona una guía completa y detallada para entender cada componente entregado y cómo ejecutar correctamente la aplicación MinExt-ADAII.