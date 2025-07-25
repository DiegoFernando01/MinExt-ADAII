% MinExt - Minimización del Extremismo en Población
% Grupo 9 - Análisis y diseño de algoritmos II - 2025/1

% ==================== PARÁMETROS DE ENTRADA ====================

int: n; % número total de personas
int: m; % número de opiniones posibles
array[1..m] of int: p; % distribución inicial por opinión
array[1..m] of float: ext; % valores de extremismo por opinión
array[1..m] of float: ce; % costos extra por mover hacia opinión
array[1..m, 1..m] of float: c; % matriz de costos de movimiento entre opiniones
float: ct; % costo total máximo permitido
int: maxM; % número máximo de movimientos permitidos

% ==================== VARIABLES DE DECISIÓN ====================

% número de personas que se mueven de opinión i a opinión j
array[1..m, 1..m] of var 0..n: x;

% variables binarias para detectar movimientos hacia opiniones vacías
array[1..m] of var 0..1: delta;

% número final de personas por opinión
array[1..m] of var 0..n: f;

% ==================== RESTRICCIONES ====================

% 1. conservación de población por origen
constraint forall(i in 1..m) (
    sum(j in 1..m) (x[i,j]) <= p[i]
);

% 2. no se puede mover de una opinión a sí misma
constraint forall(i in 1..m) (
    x[i,i] = 0
);

% 3. cálculo del número final de personas por opinión
constraint forall(i in 1..m) (
    f[i] = p[i] + sum(j in 1..m) (x[j,i]) - sum(j in 1..m) (x[i,j])
);

% 4. restricción de costo total
constraint (
    sum(i in 1..m, j in 1..m) (x[i,j] * c[i,j]) + 
    sum(i in 1..m, j in 1..m where p[j] = 0) (x[i,j] * ce[j])
) <= ct;

% 5. restricción de movimientos máximos
constraint sum(i in 1..m, j in 1..m) (x[i,j] * abs(j - i)) <= maxM;

% ==================== FUNCIÓN OBJETIVO ==========================

% minimizar el extremismo total final
var float: extremismo_total = sum(i in 1..m) (f[i] * ext[i]);

% ==================== ESTRATEGIA DE BÚSQUEDA ====================

solve minimize extremismo_total;

% ==================== SALIDA ==========================

output [
    "=== SOLUCIÓN MINEXT ===\n",
    "Extremismo Total: ", show_float(6,3,extremismo_total), "\n\n",
    
    "=== MOVIMIENTOS ===\n"
] ++
[ if fix(x[i,j]) > 0 then
    "Mover " ++ show(x[i,j]) ++ " personas: Opinión " ++ show(i) ++ " → Opinión " ++ show(j) ++ "\n"
  else ""
  endif | i in 1..m, j in 1..m ] ++
[
    "\n=== DISTRIBUCIÓN FINAL ===\n"
] ++
[ "Opinión " ++ show(i) ++ ": " ++ show(f[i]) ++ " personas\n" | i in 1..m ] ++
[
    "\n=== RECURSOS UTILIZADOS ===\n",
    "Costo total: ", show_float(6,2,sum(i in 1..m, j in 1..m)(fix(x[i,j]) * c[i,j]) + sum(i in 1..m where p[i] = 0)(fix(delta[i]) * ce[i])), " / ", show_float(6,2,ct), "\n",
    "Movimientos: ", show(sum(i in 1..m, j in 1..m)(fix(x[i,j]))), " / ", show(maxM), "\n"
];
