<p align='center'>
  <img width='200' heigth='225' src='https://user-images.githubusercontent.com/62605744/171186764-43f7aae0-81a9-4b6e-b4ce-af963564eafb.png'>
</p>

---



# Proyecto #2 - El Problema de Minimizar el Extremismo Presente en una Población

## Universidad del Valle - Escuela de Ingeniería de Sistemas y Computación

- **Asignatura:** Análisis y diseño de algoritmos II
- **Semestre:** 2025-I
- **Profesor:** Jesús Alexander Aranda Bueno Ph.D.

---

## Autores

| Nombre                  | Código    | Email                                |
| ----------------------- | --------- | ------------------------------------ |
| Diego Fernando Victoria | 202125877 | diego.victoria@correounivalle.edu.co |
| Janiert Sebastián Salas | 201941265 | janiert.salas@correounivalle.edu.co  |
| Junior Orlando Cantor   | 202224949 | junior.cantor@correounivalle.edu.co  |
| Kevin Jordan Alzate     | 202228507 | kevin.jordan@correounivalle.edu.co   |

---

## Descripción del Proyecto MinExt
MinExt-ADAII es un proyecto desarrollado para la asignatura de Analisís y Desarrollo de Algoritmos II, enfocado en la minimización del extremismo en una población mediante técnicas de optimización combinatoria. Utiliza MiniZinc para modelar el problema y Python para la gestión de datos y la interfaz gráfica.

---

## Estructura del Proyecto

### Carpetas principales
- **DatosProyecto/**: Contiene los datos originales en formato de texto plano (.txt). Estos archivos representan las instancias del problema en su forma inicial.
- **DatosDZN/**: Contiene los datos convertidos al formato `.dzn` compatible con MiniZinc, generados a partir de los archivos en `DatosProyecto`.
- **MisInstancias/**: Contiene instancias personalizadas o adicionales para pruebas específicas.
- **ProyectoGUIFuentes/**: Código fuente de la interfaz gráfica del proyecto, incluyendo el archivo principal `main.py`.

### Archivos principales
- **Proyecto.mzn**: Modelo MiniZinc que define el problema de minimización del extremismo. Contiene la definición de parámetros, variables, restricciones y la función objetivo para minimizar el extremismo total en la población.
- **generar_datosDZN.py**: Script en Python que convierte los archivos de datos originales en `DatosProyecto` al formato `.dzn` para ser usados por MiniZinc.
- **README.md**: Este archivo, que contiene la documentación del proyecto.
- **requirements.txt**: Archivo con las dependencias necesarias para ejecutar el proyecto en Python.

- **ConvertirArchivos/**
  - README.md: Documentación específica de esta carpeta.
  - interfaz.py: Código para la interfaz relacionada con la conversión.
  - utils.py: Funciones auxiliares para la conversión y procesamiento de archivos.

---

## Descripción del archivo Proyecto.mzn

Este archivo contiene el modelo MiniZinc para el problema de minimización del extremismo en la población. Define:
- Parámetros de entrada como el número de personas, opiniones posibles, distribución inicial, valores de extremismo, costos y restricciones.
- Variables de decisión que representan los movimientos de personas entre opiniones.
- Restricciones para asegurar la conservación de población, costos máximos y movimientos permitidos.
- Función objetivo para minimizar el extremismo total final.
- Estrategia de búsqueda y formato de salida para mostrar resultados.

---

## Instrucciones de Instalación y Uso

### Requisitos previos
- Git instalado para clonar el repositorio.
- Python 3.x instalado.
- MiniZinc instalado y agregado al PATH del sistema.

### Pasos
1. Clonar el repositorio:
```bash
git clone https://github.com/DiegoFernando01/MinExt-ADAII
```
2. Convertir los datos al formato `.dzn`:
```bash
python generar_datosDZN.py
```
3. Ejecutar la interfaz gráfica:
```bash
python ProyectoGUIFuentes/main.py
```
---

## Licencia
Este proyecto está bajo la Licencia MIT.