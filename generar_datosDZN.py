"""
Generador de archivos de datos para el modelo MinExt
Convierte archivos de texto del formato especificado a archivos .dzn para MiniZinc
"""

import os
import sys
from pathlib import Path

def parse_data_file(file_path):
  """
  Parsea un archivo de datos en formato plano y retorna los parámetros
  """
  with open(file_path, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]
  
  # Línea 1: n (número de personas)
  n = int(lines[0])
  
  # Línea 2: m (número de opiniones)
  m = int(lines[1])
  
  # Línea 3: distribución inicial p[i]
  p = [int(x) for x in lines[2].split(',')]
  
  # Línea 4: valores de extremismo ext[i]
  ext = [float(x) for x in lines[3].split(',')]
  
  # Línea 5: costos extra ce[i]
  ce = [float(x) for x in lines[4].split(',')]
  
  # Líneas 6 a 5+m: matriz de costos c[i][j]
  c = []
  for i in range(5, 5 + m):
    row = [float(x) for x in lines[i].split(',')]
    c.append(row)
  
  # Líneas finales: ct y maxM (pueden estar en líneas separadas)
  if len(lines) > 5 + m + 1:
    # ct y maxM en líneas separadas
    ct = float(lines[5 + m])
    maxM = int(lines[5 + m + 1])
  else:
    # ct y maxM en la misma línea
    last_line = lines[5 + m].split()
    ct = float(last_line[0])
    maxM = int(last_line[1])
  
  return {
    'n': n,
    'm': m,
    'p': p,
    'ext': ext,
    'ce': ce,
    'c': c,
    'ct': ct,
    'maxM': maxM
  }

def generate_dzn_file(data, output_path):
  """
  Genera un archivo .dzn a partir de los datos parseados
  """
  with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f"% Archivo de datos generado automáticamente\n")
    f.write(f"% MinExt - Minimización del Extremismo\n\n")
    
    f.write(f"n = {data['n']};\n")
    f.write(f"m = {data['m']};\n\n")
    
    f.write("% Distribución inicial de personas por opinión\n")
    f.write(f"p = {data['p']};\n\n")
    
    f.write("% Valores de extremismo por opinión\n")
    f.write(f"ext = {data['ext']};\n\n")
    
    f.write("% Costos extra por mover hacia opinión inicialmente vacía\n")
    f.write(f"ce = {data['ce']};\n\n")
    
    f.write("% Matriz de costos de movimiento entre opiniones\n")
    f.write("c = array2d(1..m, 1..m, [")
    values = []
    for i, row in enumerate(data['c']):
      for j, val in enumerate(row):
        values.append(str(val))
    f.write(", ".join(values))
    f.write("]);\n\n")
    
    f.write("% Restricciones de recursos\n")
    f.write(f"ct = {data['ct']};\n")
    f.write(f"maxM = {data['maxM']};\n")

def process_all_instances():
  """
  Procesa todas las instancias de prueba disponibles
  """
  base_dir = Path(__file__).parent
  datos_dir = base_dir / "DatosProyecto"
  
  if not datos_dir.exists():
    print(f"Error: Directorio {datos_dir} no encontrado")
    return

  print("PROCESANDO INSTANCIAS .TXT DE MINEXT")
  # Asegura que exista el directorio de salida de datos .dzn
  dzn_dir = base_dir / "DatosDZN"
  if not dzn_dir.exists():
    dzn_dir.mkdir()
  # Procesar todos los archivos .txt en DatosProyecto
  for txt_file in datos_dir.glob("*.txt"):
    if txt_file.name == "enunciado.txt":
      continue  # Ya tenemos el archivo manual para el enunciado
      
    print(f"Procesando: {txt_file.name}")
    
    try:
      # Parsear datos
      data = parse_data_file(txt_file)
      
      # Generar archivo .dzn en DatosDZN
      dzn_file = dzn_dir / f"{txt_file.stem}.dzn"
      generate_dzn_file(data, dzn_file)
      
      print(f"  ✓ Generado: DatosDZN/{dzn_file.name}")
      
    except Exception as e:
      print(f"  ❌ Error procesando {txt_file.name}: {e}")
      print()

def main():
  """
  Función principal
  """
  if len(sys.argv) > 1:
    # Procesar archivo específico
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
      print(f"Error: Archivo {input_file} no encontrado")
      return
    
    try:
      data = parse_data_file(input_file)
      output_file = input_file.replace('.txt', '.dzn')
      generate_dzn_file(data, output_file)
      
      print(f"Archivo generado: {output_file}")
      
    except Exception as e:
      print(f"Error: {e}")
  else:
    # Procesar todas las instancias
    process_all_instances()

if __name__ == "__main__":
  main()
