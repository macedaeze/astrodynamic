import math
import unittest

def getHyperbolicAnomaly(meanAnomaly, eccentricity):
    """
    Funcion que calcula la anomalia hiperbólica a partir de la anomalia media y la excentricidad.
    
    Parametros:
    meanAnomaly (float): Anomalia media [en radianes]
    eccentricity (float): Excentricidad [adimensional]
    
    Retorna:
    float: Anomalia hiperbólica [en radianes]
    """
    
    # Inicializamos la anomalia hiperbólica

    if eccentricity < 1.6:
        if (-math.pi < meanAnomaly < 0) or (meanAnomaly > math.pi):
            hyperbolicAnomaly = meanAnomaly - eccentricity
        else:
            hyperbolicAnomaly = meanAnomaly + eccentricity
    else:
        hyperbolicAnomaly = meanAnomaly

    hyperbolicAnomaly = meanAnomaly / (eccentricity - 1)


    # Itero para encontrar la anomalia hiperbólica
    max_iter = 500
    for _ in range(max_iter):
        delta = (meanAnomaly - eccentricity * math.sinh(hyperbolicAnomaly) + hyperbolicAnomaly) / (eccentricity * math.cosh(hyperbolicAnomaly) - 1)
        hyperbolicAnomaly += delta
        if abs(delta) < 1e-6:
            return hyperbolicAnomaly
    raise ValueError("No convergió despues de {} iteraciones".format(max_iter))
    
#TEST UNITARIOS
class TestGetHyperbolicAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getHiperbolicAnomaly.
        """
        test_cases = [
            # ( e,    M,         expected )
            (2.4,   4.108,       1.601376),         # Ejemplo en Vallado p71

        ]

        for eccentricity, meanAnomaly, expected in test_cases:
            with self.subTest(eccentricity=eccentricity, meanAnomaly=meanAnomaly):
                result = getHyperbolicAnomaly(meanAnomaly, eccentricity)
                self.assertAlmostEqual(result, expected, places=3)

if __name__ == "__main__":
    
    unittest.main()
