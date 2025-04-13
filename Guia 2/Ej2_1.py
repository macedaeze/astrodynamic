import numpy as np
import unittest
from math import pi

def getEccentricAnomaly(ecentricity, meanAnomaly, errTolerance=1e-6):
    """
    Funcion que calcula el anomalia excentrica a partir de la excentricidad y la anomalia media.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    M (float): Anomalia media [en radianes]
    
    Retorna:
    float: Anomalia excentrica [en radianes]
    """

    # Maximo de iteraciones para evitar un bucle infinito
    max_iter = 500


    if (-np.pi < meanAnomaly < 0) or (meanAnomaly > np.pi):
        eccentricAnomaly = meanAnomaly - ecentricity
    else:
        eccentricAnomaly = meanAnomaly + ecentricity

    # Aca el algoritmo del libro dice que evaluemos en la condicion si el error es aceptable pero en la practica preferi poner un maximo de iteraciones para evitar un bucle ininito
    # en caso de que no converja.
    for _ in range(max_iter):
        delta = (meanAnomaly - eccentricAnomaly + ecentricity * np.sin(eccentricAnomaly)) / (1 - ecentricity * np.cos(eccentricAnomaly))
        eccentricAnomaly += delta
        if abs(delta) < errTolerance:
            return eccentricAnomaly
        
    raise ValueError("No convergió despues de {} iteraciones".format(max_iter))


def main():
    
    # Pedimos al usuario que ingrese los valores de la excentricidad y la anomalia media
    ecentricity = float(input("Ingrese la excentricidad: "))
    meanAnomaly = float(input("Ingrese la anomalia media [en radianes]: "))
    # Lo comento porque al ser un numero chico es complicado ponerlo por teclado
    # errTolerance = float(input("Ingrese la tolerancia: "))

    # Llamamos a la funcion y mostramos el resultado
    eccentricAnomaly = getEccentricAnomaly(ecentricity, meanAnomaly)
    print(f"Eccentric Anomaly: {eccentricAnomaly:.6f} rad")

#TEST UNITARIOS
class TestGetEccentricAnomaly(unittest.TestCase):

    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getEccentricAnomaly.
        """
        test_cases = [
            # ( e,    M,         expected_E )
            (0.0,   0.0,       0.0),         # trivial - E=M=0
            (0.0,   1.5708,    1.5708),      # e=0 => E=M=π/2
            (0.0,   3.1416,    3.1416),      # e=0 => E=M=π
            (0.1,   1.0,       1.0885),      # calculado con tu iterador
            (0.3,   0.5,       0.6912),
            (0.5,   1.5708,    2.0211),      # ~π/2
            (0.5,   3.1416,    3.1416),      # E=M=π - e=0.5 pero M=π produce E=π
        ]

        for e, M, expected in test_cases:
            with self.subTest(e=e, M=M):
                result = getEccentricAnomaly(e, M)
                self.assertAlmostEqual(result, expected, places=3)

if __name__ == "__main__":
    #Se puede comentar el main aca para probar solamente los tests unitarios
    main()
    unittest.main()