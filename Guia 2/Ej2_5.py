import math
import unittest
import numpy as np

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
        
        SenEccentricAnomaly =  np.sin(trueAnomaly) * np.sqrt(1 - eccentricity**2) / (1 + eccentricity * np.cos(trueAnomaly) )
        CosEccentricAnomaly = (eccentricity + np.cos(trueAnomaly)) / (1 + eccentricity * np.cos(trueAnomaly) )
        eccentricAnomaly = np.arctan2(SenEccentricAnomaly, CosEccentricAnomaly)
    elif eccentricity == 1.0:
        # Para el caso parabolico
        eccentricAnomaly = np.tan(trueAnomaly / 2)
    elif eccentricity > 1.0:
        # Para el caso hiperbólico
        eccentricAnomaly = np.asinh(math.sin(trueAnomaly) * math.sqrt(eccentricity**2 - 1) / 1 + eccentricity * math.cos(trueAnomaly) )
    else:
        raise ValueError("La excentricidad debe ser mayor o igual a 0.")
    return eccentricAnomaly


#TEST UNITARIOS
class TestGetEccentricAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getEccentricAnomaly.
        """
        test_cases = [
            # ( e,  trueAnom,  expected )
            (0.0,   0.0,       0.0),         
            (0.5,   1.0472,    0.6435),     
            (1.0,   1.0472,    0.5773), 
            (1.5,   1.0472,    1.3100),  
        ]

        for eccentricity, trueAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, trueAnomaly=trueAnomaly):
                result = getEccentricAnomaly(eccentricity, trueAnomaly)
                self.assertAlmostEqual(result, expected, places=3)


if __name__ == "__main__":
    unittest.main()