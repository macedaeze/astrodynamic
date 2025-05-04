"""

Elementos orbitales
Para describir la órbita completa, usamos seis parámetros llamados "elementos orbitales":

Semieje mayor (a): Define el tamaño de la elipse
Excentricidad (e): Define la forma de la elipse (0 = círculo, 0<e<1 = elipse)
Inclinación (i): Ángulo entre el plano orbital y el plano de referencia
Ascensión recta del nodo ascendente (RAAN): Orienta el plano orbital en el espacio
Argumento del periapsis (ω): Orienta la elipse en el plano orbital
Anomalía verdadera (ν): Define la posición del satélite en la órbita

La Ecuación de Kepler
En lugar de resolver directamente las ecuaciones diferenciales del movimiento, usamos la ecuación de Kepler para propagar la órbita:
M = E - e * sin(E)
Donde:

M es la anomalía media (aumenta linealmente con el tiempo)
E es la anomalía excéntrica
e es la excentricidad

La anomalía media avanza a una velocidad constante:
M = M₀ + n * t
Donde:

M₀ es la anomalía media inicial
n = √(μ/a³) es el movimiento medio
t es el tiempo transcurrido

El proceso de propagación
Para propagar la órbita sin integración numérica:

Convertimos posición y velocidad iniciales en elementos orbitales
Calculamos la anomalía media en el tiempo deseado
Resolvemos la ecuación de Kepler para obtener la anomalía excéntrica
Convertimos la anomalía excéntrica a anomalía verdadera
Calculamos la posición y velocidad desde la anomalía verdadera

"""