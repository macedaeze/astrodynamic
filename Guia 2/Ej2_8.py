import math
from Ej2_1 import getEccentricAnomaly
from Ej2_2 import getMeanAnomaly
import unittest
import numpy as np


def getMeanAnomalyFromTrue(eccentricity, trueAnomaly):
    """
    Funcion que calcula la anomalia media a partir de la excentricidad y la anomalia verdadera.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    trueAnomaly (float): Anomalia verdadera [en radianes]
    
    Retorna:
    float: Anomalia media [en radianes]
    """

    if eccentricity < 1.0 and eccentricity > 0.0:
        # Para el caso eliptico
        eccentricAnomaly = getEccentricAnomaly(eccentricity, trueAnomaly)
        print("Eccentric Anomaly: ", eccentricAnomaly)
        meanAnomaly = getMeanAnomaly(eccentricity, eccentricAnomaly)
        print("Mean Anomaly: ", meanAnomaly)

    else:
        raise ValueError("La excentricidad debe ser mayor o igual a 0 y menor o igual a 1.")
    return meanAnomaly

#TEST UNITARIOS

class TestGetMeanAnomalyFromTrue(unittest.TestCase):
    """
    Clase de test para verificar la función getMeanAnomaly.
    """
    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getMeanAnomaly.
        """
        test_cases = [
            # ( e,  trueAnomaly,    expected )
            (0.1,   0.0,            0.0),  
            (0.5,   1.0472,         1.0472), 
            (0.9,   1.0472,         1.0472),  
        ]

        for eccentricity, trueAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, trueAnomaly=trueAnomaly):
                result = getMeanAnomalyFromTrue(eccentricity, trueAnomaly=trueAnomaly)
                self.assertAlmostEqual(result, expected, places=3)


if __name__ == "__main__":
    unittest.main()