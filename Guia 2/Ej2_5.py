import math
import unittest

def getEccentricAnomaly(eccentricity, trueAnomaly):
    """
    Funcion que calcula la anomalia excentrica a partir de la excentricidad y la anomalia verdadera.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    nu (float): Anomalia verdadera [en radianes]
    
    Retorna:
    float: Anomalia excentrica [en radianes]
    """
    
    if eccentricity < 1.0:
        # Para el caso eliptico
        eccentricAnomaly = math.asin(math.sin(trueAnomaly) * math.sqrt(1 - eccentricity**2) / (1 + eccentricity * math.cos(trueAnomaly) ) )
    elif eccentricity == 1.0:
        # Para el caso parabolico
        eccentricAnomaly = math.tan(trueAnomaly / 2)
    elif eccentricity > 1.0:
        # Para el caso hiperbólico
        eccentricAnomaly = math.asinh(math.sin(trueAnomaly) * math.sqrt(eccentricity**2 - 1) / 1 + eccentricity * math.cos(trueAnomaly) )
    else:
        raise ValueError("La excentricidad debe ser mayor o igual a 0 y menor o igual a 1.")
    
    return eccentricAnomaly


#TEST UNITARIOS
class TestGetEccentricAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getEccentricAnomaly.
        """
        test_cases = [
            # ( e,    nu,         expected_E )
            (0.0,   0.0,       0.0),         # trivial - E=M=0
            (0.5,   1.0472,    0.6435),      # e=0.5 => E=π/6
            (1.0,   1.0472,    0.5773),      # e=1 => E=π/3
            (1.5,   1.0472,    1.3100),      # e>1 => E=π/3
        ]

        for eccentricity, trueAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, trueAnomaly=trueAnomaly):
                result = getEccentricAnomaly(eccentricity, trueAnomaly)
                self.assertAlmostEqual(result, expected, places=3)


if __name__ == "__main__":
    unittest.main()