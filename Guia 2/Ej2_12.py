from Ej2_8 import getMeanAnomalyFromTrue
import numpy as np
import unittest


def getTimeOfFlight(trueAnomaly0, trueAnomalyf, eccentricity, semiMajorAxis):
    """
    Calculate the time of flight between two true anomalies.

    Parameters:
    trueAnomaly0 (float): Initial true anomaly in radians.
    trueAnomalyf (float): Final true anomaly in radians.
    eccentricity (float): Eccentricity of the orbit.
    semiMajorAxis (float): Semi-major axis of the orbit in kilometers.

    Returns:
    float: Time of flight in seconds.
    """
    # Constants
    mu = 398600  # Gravitational parameter for Earth in km^3/s^2

    if eccentricity < 1 and eccentricity > 0:
        meanAnomaly0 = getMeanAnomalyFromTrue(eccentricity, trueAnomaly0) # This method uses the true anomaly to calculate the eccentric anomaly and then the mean anomaly
        meanAnomalyf = getMeanAnomalyFromTrue(eccentricity, trueAnomalyf)
        meanVelocity = np.sqrt(mu / semiMajorAxis**3)
        tof = (meanAnomalyf - meanAnomaly0) / meanVelocity
        return tof
    else:
        raise ValueError("Eccentricity must be between 0 and 1 for elliptical orbits.")
    

# TEST UNITARIOS

class TestGetTimeOfFlight(unittest.TestCase):
    """
    Clase de test para verificar la función getTimeOfFlight.
    """
    def test_matrix_of_cases(self):
        """
        Matriz de casos sencillos para verificar la función getTimeOfFlight.
        """
        test_cases = [
            # ( trueAnomaly0,  trueAnomalyf,  eccentricity,  semiMajorAxis,  expected )
            (0.0,            1.0472,         0.1,          10000,         1394.6161),  
            (0.0,            1.0472,         0.5,          10000,         544.0775),  
            (0.0,            1.0472,         0.9,          10000,         46.0417),  
        ]

        for trueAnomaly0, trueAnomalyf, eccentricity, semiMajorAxis, expected in test_cases:
            with self.subTest(trueAnomaly0=trueAnomaly0, trueAnomalyf=trueAnomalyf):
                result = getTimeOfFlight(trueAnomaly0=trueAnomaly0,
                                          trueAnomalyf=trueAnomalyf,
                                          eccentricity=eccentricity,
                                          semiMajorAxis=semiMajorAxis)
                self.assertAlmostEqual(result, expected, places=4)


if __name__ == "__main__":
    unittest.main()