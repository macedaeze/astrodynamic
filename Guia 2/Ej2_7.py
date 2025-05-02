from Ej2_2 import getMeanAnomaly
import math
import unittest

# Itero la funcion del 2_6 para que sea mas generica y calcule la anomalia verdadera en base a distintos casos

def getTrueAnomaly(eccentricity, eccentricAnomaly = None, meanAnomaly = None, semilactusRectum = None, rDistance = None):
    """
    Funcion que calcula la anomalia verdadera a partir de la excentricidad y la anomalia excentrica.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    E (float): Anomalia excentrica [en radianes]
    
    Retorna:
    float: Anomalia verdadera [en radianes]
    """
    
    if eccentricAnomaly == None:
        eccentricAnomaly = getMeanAnomaly(eccentricity, meanAnomaly)

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

    """
    Clase de test para verificar la función getTrueAnomaly.
    """
    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getTrueAnomaly.
        """
        test_cases = [
            # ( e,  meanAnomaly,       expected )
            (0.0,   0.0,            0.0),  
            (0.5,   1.0472,         0.36217),  
            (1.5,   1.0472,         0.54617), 
        ]

        for eccentricity, meanAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, trueAnomaly=meanAnomaly):
                result = getTrueAnomaly(eccentricity, meanAnomaly=meanAnomaly)
                self.assertAlmostEqual(result, expected, places=3)

    def test_parabolicCase(self):
        """
        Caso parabolico para verificar la función getTrueAnomaly.
        """
        eccentricity = 1.0
        meanAnomaly = 1.0472
        semilactusRectum = 1000000.0
        rDistance = 2000000.0
        expected = 0.0907
        result = getTrueAnomaly(eccentricity, meanAnomaly=meanAnomaly, semilactusRectum = semilactusRectum, rDistance = rDistance)
        self.assertAlmostEqual(result, expected, places=3)

if __name__ == "__main__":
    unittest.main()