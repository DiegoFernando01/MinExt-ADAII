% MinExt - Minimización del Extremismo en Población
% Grupo 9 - Análisis y diseño de algoritmos II - 2025/1

% ==================== PARÁMETROS DE ENTRADA ====================

% número total de personas
int: n;

% número de opiniones posibles
int: m;

% distribución inicial por opinión
array[1..m] of int: p;

% valores de extremismo por opinión
array[1..m] of float: ext;

% costos extra por mover hacia opinión
array[1..m] of float: ce;

% matriz de costos de movimiento entre opiniones
array[1..m, 1..m] of float: c;

% costo total máximo permitido
float: ct;

% número máximo de movimientos permitidos
int: maxM;

% ==================== VARIABLES DE DECISIÓN ====================

% número de personas que se mueven de opinión i a opinión j
array[1..m, 1..m] of var 0..n: x;

% variables binarias para detectar movimientos hacia opiniones vacías
array[1..m] of var 0..1: delta;

% número final de personas por opinión
array[1..m] of var 0..n: f;
