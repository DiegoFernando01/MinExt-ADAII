#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilidades para MinExt GUI
"""

import os
import sys
from pathlib import Path

def check_minizinc_installation():
    """
    Verifica si MiniZinc está instalado y disponible en el PATH
    Returns: (bool, str) - (está_instalado, mensaje)
    """
    try:
        import subprocess
        result = subprocess.run(['minizinc', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            return True, f"MiniZinc encontrado: {version}"
        else:
            return False, "MiniZinc no responde correctamente"
    except FileNotFoundError:
        return False, "MiniZinc no está instalado o no está en el PATH"
    except subprocess.TimeoutExpired:
        return False, "MiniZinc no responde (timeout)"
    except Exception as e:
        return False, f"Error verificando MiniZinc: {str(e)}"

def get_project_paths():
    """
    Obtiene las rutas importantes del proyecto
    Returns: dict con las rutas
    """
    # Detectar la ruta base del proyecto
    current_file = Path(__file__).resolve()
    
    # Buscar hacia arriba hasta encontrar el directorio con Proyecto.mzn
    project_dir = current_file.parent
    while project_dir != project_dir.parent:
        if (project_dir / "Proyecto.mzn").exists():
            break
        project_dir = project_dir.parent
    else:
        # Si no se encuentra, usar el directorio padre del actual
        project_dir = current_file.parent.parent
    
    return {
        'project': project_dir,
        'model': project_dir / "Proyecto.mzn",
        'dzn_dir': project_dir / "DatosDZN",
        'datos_dir': project_dir / "DatosProyecto",
        'gui_dir': current_file.parent
    }

def validate_dzn_file(file_path):
    """
    Valida que un archivo .dzn tenga la estructura esperada
    Returns: (bool, list) - (es_válido, errores)
    """
    required_params = ['n', 'm', 'p', 'ext', 'ce', 'c', 'ct', 'maxM']
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar parámetros requeridos
        for param in required_params:
            if f"{param} =" not in content:
                errors.append(f"Parámetro faltante: {param}")
        
        # Verificaciones adicionales
        if "array2d" not in content:
            errors.append("Matriz de costos (c) no encontrada")
        
        return len(errors) == 0, errors
        
    except Exception as e:
        return False, [f"Error leyendo archivo: {str(e)}"]

def format_solution_output(raw_output):
    """
    Formatea la salida del solver para una mejor presentación
    """
    if not raw_output.strip():
        return "Sin resultado"
    
    lines = raw_output.split('\n')
    formatted_lines = []
    
    in_solution_section = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Mejorar formato de secciones
        if line.startswith("=== "):
            formatted_lines.append(f"\n{line}")
            in_solution_section = True
        elif line.startswith("Extremismo Total:"):
            formatted_lines.append(f"🎯 {line}")
        elif line.startswith("Mover ") and "personas:" in line:
            # Formatear movimientos
            formatted_lines.append(f"📋 {line}")
        elif line.startswith("Opinión ") and "personas" in line:
            # Formatear distribución final
            formatted_lines.append(f"👥 {line}")
        elif line.startswith("Costo total:"):
            formatted_lines.append(f"💰 {line}")
        elif line.startswith("Movimientos:"):
            formatted_lines.append(f"🔄 {line}")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def extract_solution_metrics(output):
    """
    Extrae métricas clave de la solución
    Returns: dict con las métricas
    """
    metrics = {
        'extremismo_total': None,
        'costo_usado': None,
        'costo_limite': None,
        'movimientos_usados': None,
        'movimientos_limite': None,
        'num_movimientos_activos': 0
    }
    
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Extremismo total
        if "Extremismo Total:" in line:
            try:
                metrics['extremismo_total'] = float(line.split(":")[-1].strip())
            except:
                pass
        
        # Costo total
        elif "Costo total:" in line:
            try:
                parts = line.split("Costo total:")[-1].strip().split("/")
                if len(parts) >= 2:
                    metrics['costo_usado'] = float(parts[0].strip())
                    metrics['costo_limite'] = float(parts[1].strip())
            except:
                pass
        
        # Movimientos
        elif "Movimientos:" in line:
            try:
                parts = line.split("Movimientos:")[-1].strip().split("/")
                if len(parts) >= 2:
                    metrics['movimientos_usados'] = int(parts[0].strip())
                    metrics['movimientos_limite'] = int(parts[1].strip())
            except:
                pass
        
        # Contar movimientos activos
        elif line.startswith("Mover ") and "personas:" in line:
            metrics['num_movimientos_activos'] += 1
    
    return metrics

def create_solution_summary(metrics):
    """
    Crea un resumen textual de la solución
    """
    if not metrics['extremismo_total']:
        return "No se encontró solución válida"
    
    summary = f"Extremismo Total: {metrics['extremismo_total']:.3f}\n"
    
    if metrics['costo_usado'] is not None:
        porcentaje_costo = (metrics['costo_usado'] / metrics['costo_limite']) * 100
        summary += f"Costo: {metrics['costo_usado']:.2f} / {metrics['costo_limite']:.2f} ({porcentaje_costo:.1f}%)\n"
    
    if metrics['movimientos_usados'] is not None:
        porcentaje_mov = (metrics['movimientos_usados'] / metrics['movimientos_limite']) * 100
        summary += f"Movimientos: {metrics['movimientos_usados']} / {metrics['movimientos_limite']} ({porcentaje_mov:.1f}%)\n"
    
    summary += f"Tipos de movimiento: {metrics['num_movimientos_activos']}"
    
    return summary
