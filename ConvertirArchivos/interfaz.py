#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI para el Generador de archivos DZN
Interfaz gráfica simple para procesar archivos .txt y convertirlos a .dzn
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path
import threading

# Importar las funciones del generador principal
from utils import parse_data_file, generate_dzn_file

class GeneradorDZNGUI:
  def __init__(self, root):
    self.root = root
    self.root.title("Generador de archivos DZN - MinExt")
    self.root.geometry("800x600")
    
    # Configurar el directorio base del proyecto
    self.project_dir = Path(__file__).parent.parent
    self.dzn_dir = self.project_dir / "DatosDZN"
    self.source_dirs = [
        self.project_dir / "DatosProyecto",
        self.project_dir / "MisInstancias"
    ]
    
    # Variables
    self.processing = False
    
    self.setup_ui()
    
  def setup_ui(self):
    """Configura la interfaz de usuario"""
    # Marco principal
    main_frame = ttk.Frame(self.root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Configurar el redimensionamiento
    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(3, weight=1)
    
    # Título
    title_label = ttk.Label(main_frame, text="Generador de Archivos DZN", 
                           font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    # Botones de acción
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, columnspan=3, pady=20)
    
    self.process_button = ttk.Button(button_frame, text="Convertir Todas las Instancias", 
                                    command=self.process_files, state="normal")
    self.process_button.pack(side=tk.LEFT, padx=5)
    
    self.clear_button = ttk.Button(button_frame, text="Limpiar", 
                                  command=self.clear_log)
    self.clear_button.pack(side=tk.LEFT, padx=5)
    
    # Área de log
    log_frame = ttk.LabelFrame(main_frame, text="Log de procesamiento", padding="5")
    log_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)
    
    self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
    self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Barra de progreso
    self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
    self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    # Información inicial
    self.log_message("=== Generador de archivos DZN para MinExt ===")
    self.log_message("Presione 'Convertir Todas las Instancias' para procesar los archivos.")
    self.log_message(f"Los archivos .dzn se generarán en: {self.dzn_dir}")
    self.log_message("")
    
    # Verificar si existe la carpeta DatosDZN
    if not self.dzn_dir.exists():
      self.dzn_dir.mkdir(exist_ok=True)
      self.log_message(f"✓ Creada carpeta de salida: {self.dzn_dir}")

  def process_files(self):
    """Procesa los archivos .txt de las carpetas de origen""" 
    if self.processing:
      return
      
    # Ejecutar el procesamiento en un hilo separado
    thread = threading.Thread(target=self._process_files_thread)
    thread.daemon = True
    thread.start()

  def _process_files_thread(self):
    """Hilo para procesar archivos sin bloquear la interfaz"""
    self.processing = True
    self.processing = True
    self.process_button.config(state="disabled")
    self.progress.start()
    
    try:
      all_txt_files = []
      for source_dir in self.source_dirs:
        if source_dir.exists():
          all_txt_files.extend(list(source_dir.glob("*.txt")))
        else:
          self.log_message(f"⚠️  Advertencia: El directorio {source_dir} no existe y será omitido.")

      if not all_txt_files:
        self.log_message("❌ No se encontraron archivos .txt en los directorios de origen.")
        return
      
      self.log_message(f"🚀 Iniciando procesamiento de {len(all_txt_files)} archivos...")
      self.log_message("")
      
      success_count = 0
      error_count = 0
      
      for txt_file in all_txt_files:
        try:
          self.log_message(f"📝 Procesando: {txt_file.name}")
          
          # Parsear datos del archivo
          data = parse_data_file(txt_file)
          
          # Generar archivo .dzn
          dzn_file = self.dzn_dir / f"{txt_file.stem}.dzn"
          generate_dzn_file(data, dzn_file)
          
          self.log_message(f"   ✅ Generado: {dzn_file.name}")
          success_count += 1
          
        except Exception as e:
          self.log_message(f"   ❌ Error: {str(e)}")
          error_count += 1
        
        self.log_message("")
      
      # Resumen final
      self.log_message("=" * 50)
      self.log_message(f"✅ Procesamiento completado:")
      self.log_message(f"   - Archivos procesados exitosamente: {success_count}")
      if error_count > 0:
        self.log_message(f"   - Archivos con errores: {error_count}")
      else:
        self.log_message(f"   - Sin errores")
      self.log_message(f"   - Archivos .dzn generados en: {self.dzn_dir}")
      self.log_message("")
      
      # Mostrar mensaje de éxito
      if success_count > 0:
        messagebox.showinfo("Procesamiento completado", 
                          f"Se procesaron exitosamente {success_count} archivos.\n"
                          f"Los archivos .dzn se generaron en:\n{self.dzn_dir}")
    
    except Exception as e:
      self.log_message(f"❌ Error general: {str(e)}")
      messagebox.showerror("Error", f"Error durante el procesamiento:\n{str(e)}")
    
    finally:
      self.processing = False
      self.process_button.config(state="normal")
      self.progress.stop()

  def clear_log(self):
    """Limpia el área de log"""
    self.log_text.delete(1.0, tk.END)
    self.log_message("=== Log limpiado ===")
    self.log_message("")

  def log_message(self, message):
    """Añade un mensaje al log"""
    self.log_text.insert(tk.END, message + "\n")
    self.log_text.see(tk.END)
    self.root.update_idletasks()

def main():
  """Función principal"""
  root = tk.Tk()
  app = GeneradorDZNGUI(root)
  root.mainloop()

if __name__ == "__main__":
  main()
