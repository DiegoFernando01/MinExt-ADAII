# Convertidor de Archivos TXT a DZN

Esta carpeta contiene las herramientas para convertir archivos de datos en formato `.txt` a archivos `.dzn` compatibles con MiniZinc para el proyecto MinExt.

## Archivos

- **`procesar_datos.py`** - Módulo con las funciones de conversión
- **`gui_generador_dzn.py`** - Interfaz gráfica para la conversión

## Uso Rápido

1. **Ejecutar la interfaz gráfica:**

   ```cmd
   python gui_generador_dzn.py
   ```

2. **Seleccionar carpeta** con archivos `.txt`
3. **Hacer clic** en "Procesar Archivos"
4. **Los archivos `.dzn`** se generarán en `../DatosDZN/`

## Características

✅ **Interfaz intuitiva** con log en tiempo real  
✅ **Selección flexible** de carpetas  
✅ **Procesamiento en lote** de múltiples archivos  
✅ **Manejo de errores** individual por archivo  
✅ **Indentación de 2 espacios** para mejor legibilidad

## Estructura de la Carpeta

```
ConvertirArchivosTxt-Dzn/
├── procesar_datos.py        # Funciones de conversión
├── gui_generador_dzn.py     # Interfaz gráfica
└── README.md               # Este archivo
```

## Requisitos

- Python 3.6+
- tkinter (incluido con Python)
- Carpeta `DatosDZN` en el directorio padre del proyecto
