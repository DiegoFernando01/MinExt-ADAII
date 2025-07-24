#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MinExt GUI - Interfaz gráfica para el proyecto MinExt
Grupo 9 - Análisis y diseño de algoritmos II - 2025/1
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import subprocess
import threading
import glob
import re
import time
from pathlib import Path

# Intentar importar utilidades locales
try:
  from utils import check_minizinc_installation, get_project_paths, format_solution_output, extract_solution_metrics
  UTILS_AVAILABLE = True
except ImportError:
  UTILS_AVAILABLE = False

class MinExtGUI:
  def __init__(self, root):
    self.root = root
    self.root.title("MinExt - Minimización del Extremismo")
    self.root.geometry("1000x700")
    
    # Rutas del proyecto
    if UTILS_AVAILABLE:
      paths = get_project_paths()
      self.project_dir = paths['project']
      self.dzn_dir = paths['dzn_dir']
      self.model_file = paths['model']
    else:
      self.project_dir = Path(__file__).parent.parent
      self.dzn_dir = self.project_dir / "DatosDZN"
      self.model_file = self.project_dir / "Proyecto.mzn"
    
    # Variables
    self.current_instance = None
    self.current_solution = None
    self.is_running = False
    self.demo_mode = False
    
    # Verificar MiniZinc al iniciar
    self.check_minizinc_status()
    
    self.setup_ui()
    self.load_instances()
    
  def check_minizinc_status(self):
    """Verifica el estado de MiniZinc"""
    if UTILS_AVAILABLE:
      is_installed, message = check_minizinc_installation()
      if not is_installed:
        self.demo_mode = True
        messagebox.showinfo(
          "Modo Demo", 
          f"{message}\n\nLa aplicación funcionará en modo demo con resultados simulados."
        )
    else:
      # Verificación básica sin utilidades
      try:
        subprocess.run(['minizinc', '--version'], 
                     capture_output=True, timeout=5)
      except (FileNotFoundError, subprocess.TimeoutExpired):
        self.demo_mode = True
        messagebox.showinfo(
          "Modo Demo", 
          "MiniZinc no está disponible.\nLa aplicación funcionará en modo demo."
        )
      
  def setup_ui(self):
    """Configura la interfaz de usuario"""
    # Frame principal
    main_frame = ttk.Frame(self.root, padding="10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Configurar grid weights
    self.root.columnconfigure(0, weight=1)
    self.root.rowconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)
    
    # Título
    title_text = "MinExt - Minimización del Extremismo"
    if self.demo_mode:
      title_text += " (MODO DEMO)"
    title_label = ttk.Label(main_frame, text=title_text, 
                           font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
    
    # Frame de selección de instancia
    instance_frame = ttk.LabelFrame(main_frame, text="Selección de Instancia", padding="10")
    instance_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
    instance_frame.columnconfigure(1, weight=1)
    
    ttk.Label(instance_frame, text="Instancia:").grid(row=0, column=0, padx=(0, 10))
    
    self.instance_var = tk.StringVar()
    self.instance_combo = ttk.Combobox(instance_frame, textvariable=self.instance_var, 
                                      state="readonly", width=30)
    self.instance_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
    self.instance_combo.bind('<<ComboboxSelected>>', self.on_instance_selected)
    
    # Botones de control
    button_frame = ttk.Frame(instance_frame)
    button_frame.grid(row=0, column=2)
    
    self.run_button = ttk.Button(button_frame, text="Ejecutar Modelo", 
                                command=self.run_model, style="Accent.TButton")
    self.run_button.pack(side=tk.LEFT, padx=(0, 5))
    
    self.stop_button = ttk.Button(button_frame, text="Detener", 
                                 command=self.stop_execution, state="disabled")
    self.stop_button.pack(side=tk.LEFT, padx=(0, 5))
    
    self.refresh_button = ttk.Button(button_frame, text="Limpiar", 
                                    command=self.load_instances)
    self.refresh_button.pack(side=tk.LEFT)
    
    # Notebook para las pestañas
    self.notebook = ttk.Notebook(main_frame)
    self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Pestaña de datos de entrada
    self.setup_input_tab()
    
    # Pestaña de resultados
    self.setup_results_tab()
    
    # Pestaña de salida completa
    self.setup_output_tab()
    
    # Barra de estado
    self.status_var = tk.StringVar()
    self.status_var.set("Listo")
    status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                          relief=tk.SUNKEN, anchor=tk.W)
    status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
    
    # Progress bar
    self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
    self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
  def setup_input_tab(self):
    """Configura la pestaña de datos de entrada"""
    input_frame = ttk.Frame(self.notebook)
    self.notebook.add(input_frame, text="Datos de Entrada")
    
    input_frame.columnconfigure(0, weight=1)
    input_frame.rowconfigure(0, weight=1)
    
    self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                               font=("Consolas", 10))
    self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    
  def setup_results_tab(self):
    """Configura la pestaña de resultados"""
    results_frame = ttk.Frame(self.notebook)
    self.notebook.add(results_frame, text="Mejor Solución")
    
    results_frame.columnconfigure(0, weight=1)
    results_frame.rowconfigure(1, weight=1)
    
    # Frame de resumen
    summary_frame = ttk.LabelFrame(results_frame, text="Resumen de la Solución", padding="10")
    summary_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
    summary_frame.columnconfigure(1, weight=1)
    
    # Métricas principales
    ttk.Label(summary_frame, text="Extremismo Total:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
    self.extremismo_label = ttk.Label(summary_frame, text="-", font=("Arial", 10))
    self.extremismo_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
    
    ttk.Label(summary_frame, text="Costo Utilizado:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
    self.costo_label = ttk.Label(summary_frame, text="-", font=("Arial", 10))
    self.costo_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
    
    ttk.Label(summary_frame, text="Movimientos:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)
    self.movimientos_label = ttk.Label(summary_frame, text="-", font=("Arial", 10))
    self.movimientos_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
    
    ttk.Label(summary_frame, text="Tiempo de Ejecución:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W)
    self.tiempo_label = ttk.Label(summary_frame, text="-", font=("Arial", 10))
    self.tiempo_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
    
    # Detalles de la solución
    details_frame = ttk.LabelFrame(results_frame, text="Detalles de la Solución", padding="5")
    details_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    details_frame.columnconfigure(0, weight=1)
    details_frame.rowconfigure(0, weight=1)
    
    self.results_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD, 
                                                 font=("Consolas", 10))
    self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
  def setup_output_tab(self):
    """Configura la pestaña de salida completa"""
    output_frame = ttk.Frame(self.notebook)
    self.notebook.add(output_frame, text="Salida Completa")
    
    output_frame.columnconfigure(0, weight=1)
    output_frame.rowconfigure(0, weight=1)
    
    self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                font=("Consolas", 9))
    self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    
  def load_instances(self):
    """Carga las instancias disponibles"""
    try:
      if not self.dzn_dir.exists():
        messagebox.showerror("Error", f"No se encuentra el directorio: {self.dzn_dir}")
        return
          
      # Buscar archivos .dzn
      dzn_files = list(self.dzn_dir.glob("*.dzn"))
      dzn_files.sort(key=lambda x: self.natural_sort_key(x.name))
      
      instance_names = [f.stem for f in dzn_files]
      
      self.instance_combo['values'] = instance_names
      
      if instance_names:
        self.instance_combo.set(instance_names[0])
        self.on_instance_selected()
        self.status_var.set(f"Cargadas {len(instance_names)} instancias")
      else:
        self.status_var.set("No se encontraron instancias .dzn")
          
    except Exception as e:
      messagebox.showerror("Error", f"Error cargando instancias: {str(e)}")

  def natural_sort_key(self, s):
    """Clave para ordenamiento natural (Prueba1, Prueba2, ..., Prueba10, ...)"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

  def on_instance_selected(self, event=None):
    """Maneja la selección de una instancia"""
    if not self.instance_var.get():
      return
        
    instance_name = self.instance_var.get()
    dzn_file = self.dzn_dir / f"{instance_name}.dzn"
    
    if dzn_file.exists():
      try:
        with open(dzn_file, 'r', encoding='utf-8') as f:
          content = f.read()
        
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, content)
        
        # Limpiar resultados anteriores
        self.clear_results()
        
        self.status_var.set(f"Instancia cargada: {instance_name}")
        
      except Exception as e:
        messagebox.showerror("Error", f"Error leyendo instancia: {str(e)}")
    else:
      messagebox.showerror("Error", f"No se encuentra el archivo: {dzn_file}")

  def clear_results(self):
    """Limpia los resultados anteriores"""
    self.extremismo_label.config(text="-")
    self.costo_label.config(text="-")
    self.movimientos_label.config(text="-")
    self.tiempo_label.config(text="-")
    self.results_text.delete(1.0, tk.END)
    self.output_text.delete(1.0, tk.END)

  def run_model(self):
    """Ejecuta el modelo MiniZinc"""
    if self.is_running:
      return
        
    if not self.instance_var.get():
      messagebox.showwarning("Advertencia", "Por favor selecciona una instancia")
      return
    
    if not self.model_file.exists():
      messagebox.showerror("Error", f"No se encuentra el modelo: {self.model_file}")
      return
    
    # Iniciar ejecución en hilo separado
    self.is_running = True
    self.run_button.config(state="disabled")
    self.stop_button.config(state="normal")
    self.progress.start(10)
    self.status_var.set("Ejecutando modelo...")
    
    # Limpiar resultados anteriores
    self.clear_results()
    
    self.execution_thread = threading.Thread(target=self._run_model_thread)
    self.execution_thread.daemon = True
    self.execution_thread.start()

  def _run_model_thread(self):
    """Ejecuta el modelo en un hilo separado"""
    try:
      instance_name = self.instance_var.get()
      dzn_file = self.dzn_dir / f"{instance_name}.dzn"
      
      start_time = time.time()
      
      # Ejecutar MiniZinc
      cmd = [
        "minizinc",
        "--solver", "Gecode",
        "--time-limit", "60000",  # 60 segundos
        str(self.model_file),
        str(dzn_file)
      ]
      
      # Ejecutar el comando
      process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
      )
      
      self.current_process = process
      stdout, stderr = process.communicate()
      return_code = process.returncode
      
      end_time = time.time()
      execution_time = end_time - start_time
      
      # Actualizar UI en el hilo principal
      self.root.after(0, self._update_results, stdout, stderr, execution_time, return_code)
      
    except FileNotFoundError:
      self.root.after(0, self._show_minizinc_error)
    except Exception as e:
      self.root.after(0, self._show_execution_error, str(e))

  def _show_minizinc_error(self):
    """Muestra error cuando MiniZinc no está instalado"""
    self._execution_finished()
    messagebox.showerror(
      "MiniZinc no encontrado", 
      "MiniZinc no está instalado o no está en el PATH del sistema.\n\n"
      "Para instalar MiniZinc:\n"
      "1. Descarga desde: https://www.minizinc.org/\n"
      "2. Instala y asegúrate de que esté en el PATH\n"
      "3. Reinicia la aplicación"
    )

  def _show_execution_error(self, error_msg):
    """Muestra error de ejecución"""
    self._execution_finished()
    messagebox.showerror("Error de Ejecución", f"Error ejecutando el modelo:\n{error_msg}")

  def _update_results(self, stdout, stderr, execution_time, return_code):
    """Actualiza los resultados en la UI"""
    self._execution_finished()
    
    # Mostrar salida completa
    full_output = f"=== STDOUT ===\n{stdout}\n\n=== STDERR ===\n{stderr}\n\n"
    full_output += f"=== INFO ===\nCódigo de salida: {return_code}\n"
    full_output += f"Tiempo de ejecución: {execution_time:.2f} segundos"
    
    self.output_text.delete(1.0, tk.END)
    self.output_text.insert(1.0, full_output)
    
    if return_code == 0 and stdout.strip():
      # Procesar la solución
      self._parse_solution(stdout, execution_time)
      self.status_var.set(f"Modelo ejecutado exitosamente en {execution_time:.2f}s")
    else:
      # Error en la ejecución
      error_msg = stderr if stderr.strip() else "Error desconocido"
      self.results_text.delete(1.0, tk.END)
      self.results_text.insert(1.0, f"Error en la ejecución:\n{error_msg}")
      self.status_var.set("Error en la ejecución del modelo")

  def _parse_solution(self, output, execution_time):
    """Parsea la solución del output de MiniZinc"""
    try:
      # Actualizar tiempo
      self.tiempo_label.config(text=f"{execution_time:.2f} segundos")
      
      # Formatear y mostrar resultado
      if UTILS_AVAILABLE:
        formatted_output = format_solution_output(output)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, formatted_output)
        
        # Extraer métricas
        metrics = extract_solution_metrics(output)
        
        # Actualizar labels con métricas
        if metrics['extremismo_total'] is not None:
          self.extremismo_label.config(text=f"{metrics['extremismo_total']:.3f}")
        
        if metrics['costo_usado'] is not None and metrics['costo_limite'] is not None:
          porcentaje = (metrics['costo_usado'] / metrics['costo_limite']) * 100
          self.costo_label.config(text=f"{metrics['costo_usado']:.2f} / {metrics['costo_limite']:.2f} ({porcentaje:.1f}%)")
        
        if metrics['movimientos_usados'] is not None and metrics['movimientos_limite'] is not None:
          porcentaje = (metrics['movimientos_usados'] / metrics['movimientos_limite']) * 100
          self.movimientos_label.config(text=f"{metrics['movimientos_usados']} / {metrics['movimientos_limite']} ({porcentaje:.1f}%)")
          
      else:
        # Parseo básico sin utilidades
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, output)
        
        # Extraer métricas básicas
        lines = output.split('\n')
        
        # Buscar extremismo total
        for line in lines:
          if "Extremismo Total:" in line:
            extremismo = line.split(":")[-1].strip()
            self.extremismo_label.config(text=extremismo)
            break
        
        # Buscar costo total
        for line in lines:
          if "Costo total:" in line:
            costo_part = line.split("Costo total:")[-1].strip()
            if "/" in costo_part:
              costo = costo_part.split("/")[0].strip()
              self.costo_label.config(text=costo)
            break
        
        # Buscar movimientos
        for line in lines:
          if "Movimientos:" in line:
            mov_part = line.split("Movimientos:")[-1].strip()
            if "/" in mov_part:
              movimientos = mov_part.split("/")[0].strip()
              self.movimientos_label.config(text=movimientos)
            break
      
      # Cambiar a la pestaña de resultados
      self.notebook.select(1)
      
    except Exception as e:
      self.results_text.delete(1.0, tk.END)
      self.results_text.insert(1.0, f"Error parseando la solución: {str(e)}\n\nSalida original:\n{output}")

  def _execution_finished(self):
    """Limpia el estado después de la ejecución"""
    self.is_running = False
    self.run_button.config(state="normal")
    self.stop_button.config(state="disabled")
    self.progress.stop()
    if hasattr(self, 'current_process'):
      delattr(self, 'current_process')

  def stop_execution(self):
    """Detiene la ejecución del modelo"""
    if hasattr(self, 'current_process'):
      try:
        self.current_process.terminate()
        self.status_var.set("Ejecución detenida por el usuario")
      except:
        pass
    self._execution_finished()

def main():
  """Función principal"""
  root = tk.Tk()
  
  # Configurar estilo
  style = ttk.Style()
  
  # Intentar usar un tema moderno
  try:
    style.theme_use('clam')
  except:
    pass
  
  app = MinExtGUI(root)
  
  try:
    root.mainloop()
  except KeyboardInterrupt:
    pass

if __name__ == "__main__":
  main()
