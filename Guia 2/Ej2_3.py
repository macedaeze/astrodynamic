# En este archivo se resuelve la ecuacion de Barker

import math
import unittest

def cot(x):
    """
    Funcion que calcula la cotangente de un angulo en radianes.

    Parametros:
    x (float): Angulo en radianes

    Retorna:
    float: Cotangente del angulo
    """
    return 1 / math.tan(x)

def arccot(x):
    """
    Funcion que calcula el arco cotangente de un valor.

    Parametros:
    x (float): Valor

    Retorna:
    float: Arco cotangente del valor
    """
    return math.atan(1 / x)

def getMeanMotion(semilactusRectum):
    """
    Funcion que calcula el movimiento medio a partir del semieje latus recto.

    Parametros:
    semilactusRectum (float): Semieje latus recto [en metros]

    Retorna:
    float: Movimiento medio [en radianes por segundo]
    """

    # Constante gravitacional
    G = 6.67430e-11  # m^3 kg^-1 s^-2
    M = 5.972e24  # kg (masa de la Tierra)
    Mu = G * M  # Constante gravitacional de la Tierra

    # Calculamos el movimiento medio
    meanMotion = 2 * (Mu / semilactusRectum ** 3) ** 0.5

    return meanMotion

def getParabolicAnomaly(deltaT, semilactusRectum):
    """
    Funcion que calcula la anomalia parabolica a partir del tiempo transcurrido y el semieje latus recto.

    Parametros:
    deltaT (float): Tiempo transcurrido [en segundos]
    semilactusRectum (float): Semieje latus recto [en metros]

    Retorna:
    float: Anomalia parabolica [en radianes]
    """
    meanMotion = getMeanMotion(semilactusRectum)

    s = arccot(3/2 * meanMotion * deltaT) / 2

    tanS = math.tan(s)
    w = math.atan(tanS ** (1/3))
 
    # Calculamos la anomalia parabolica
    B = 2 * cot(2 * w)

    return B


#TEST UNITARIOS
class TestgetParabolicAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getParabolicAnomaly.
        """
        test_cases = [#deltaT, semilactusRectum, expected
            (3227.244, 25512000, 0.81774), #Ejemplo del Vallado p69/70
            (1800,    20000000,  0.69274),
            (600,    15000000, 0.39226),
        ]

        for dt, p, expected in test_cases:
            with self.subTest(dt=dt, p=p):
                result = getParabolicAnomaly(dt, p)
                self.assertAlmostEqual(result, expected, places=3)



if __name__ == "__main__":
    
    unittest.main()
    