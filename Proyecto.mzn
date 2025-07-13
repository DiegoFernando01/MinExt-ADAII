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
    sum(i in 1..m where p[i] = 0) (delta[i] * ce[i])
) <= ct;

% 5. restricción de movimientos máximos
constraint sum(i in 1..m, j in 1..m) (x[i,j]) <= maxM;

% 6. activación de variables delta para opiniones inicialmente vacías
constraint forall(i in 1..m where p[i] = 0) (
    delta[i] >= bool2int(sum(j in 1..m) (x[j,i]) > 0)
);

% 7. para opiniones no vacías inicialmente, delta debe ser 0
constraint forall(i in 1..m where p[i] > 0) (
    delta[i] = 0
);
