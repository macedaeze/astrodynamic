import math
import unittest

def getTrueAnomaly(eccentricity, eccentricAnomaly, semilactusRectum = None, rDistance = None):
    """
    Funcion que calcula la anomalia verdadera a partir de la excentricidad y la anomalia excentrica.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    E (float): Anomalia excentrica [en radianes]
    
    Retorna:
    float: Anomalia verdadera [en radianes]
    """
    
    # Para el caso eliptico
    if eccentricity < 1.0:
        trueAnomaly = math.asin(math.sin(eccentricAnomaly) * math.sqrt(1 - eccentricity**2) / (1 + eccentricity * math.cos(eccentricAnomaly) ) )
    elif eccentricity == 1.0:
        # Para el caso parabolico
        trueAnomaly = math.asin(semilactusRectum*eccentricAnomaly / rDistance)
    elif eccentricity > 1.0:
        # Para el caso hiperbólico
        trueAnomaly = math.acos( (math.cosh(eccentricAnomaly) - eccentricity) / ( 1 - eccentricity * math.cosh(eccentricAnomaly) ) )
    else:
        raise ValueError("La excentricidad debe ser mayor o igual a 0.")
    
    return trueAnomaly


#TEST UNITARIOS
class TestGetTrueAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getTrueAnomaly.
        """
        test_cases = [
            # ( e,  eccentricAnom,  expected )
            (0.0,   0.0,            0.0),  
            (0.5,   1.0472,         0.6435),  
            (1.5,   1.0472,         1.6424), 
        ]

        for eccentricity, eccentricAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, eccentricAnomaly=eccentricAnomaly):
                result = getTrueAnomaly(eccentricity, eccentricAnomaly)
                self.assertAlmostEqual(result, expected, places=3)

    def test_parabolicCase(self):
        """
        Caso parabolico para verificar la función getTrueAnomaly.
        """
        eccentricity = 1.0
        eccentricAnomaly = 1.0472
        semilactusRectum = 1000000.0
        rDistance = 2000000.0
        expected = 0.55107
        result = getTrueAnomaly(eccentricity, eccentricAnomaly, semilactusRectum, rDistance)
        self.assertAlmostEqual(result, expected, places=3)


if __name__ == "__main__":
    
    unittest.main()