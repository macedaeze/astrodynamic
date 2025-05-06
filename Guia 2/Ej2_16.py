'''

=============
Ejercicio 13
=============

El objetivo de este ejercicio era calcular el período orbital de un 
satélite con altitudes dadas en el perigeo y apogeo, utilizando las
ecuaciones de la mecánica orbital.

Se utilizaron las siguientes ecuaciones:

1. Cálculo del Semieje Mayor (a):

    a = (r_perigeo + r_apogeo) / 2

    Donde r_perigeo y r_apogeo son las distancia del centro de la Tierra
    al perigeo y apogeo, respectivamente.

2. Cálculo del Período Orbital (T):

    T = 2 * pi * sqrt ( a^3 / mu )

    Donde mu es la constante gravitacional de la Tierra, tal que
    mu = 398600 km^3/s^2

=============
Ejercicio 14
=============

El objetivo de este ejercicio fue calcular el tiempo que tarda un
satélite en recorrer un segmento de su órbita (desde el semi-lactus
rectum al apogeo) a partir de las anomalías verdaderas ν.

Se utilizaron las siguientes ecuaciones:

1. Conversión de Anomalía Verdadera a Anomalía Excéntrica (E):

    E = 2 * arctan( sqrt((1-e) / (1+e)) * tan (v / 2))

    Donde e es la excentricidad de la órbita.

2. Cálculo del Tiempo Transcurrido (t):

    t = T / (2 * pi) * (E - e * sen(E))

    Donde se calcula el tiempo desde el perigeo hasta el punto
    correspondiente a la anomalía excéntrica.

=============
Ejercicio 15
=============

El objetivo de este ejercicio es calcular la anomalía verdadera del
satélite 80 minutos después del apogeo.

Se utilizaron las siguientes ecuaciones:

1. Cálculo de la Anomalía Media (M):

    M = n * Δt

    Donde n = 2pi / T es la frecuencia angular, y Δt es el tiempo
    transcurrido desde el apogeo (80 minutos convertido a segundos).

2. Ecuación de Kepler. Resolviendo la ecuación de Kepler para E:

    M = E - e * sen(E)

    Usando el método de Newton-Raphson para resolver esta ecuación
    iterativamente.

'''