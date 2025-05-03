import numpy as np
import matplotlib.pyplot as plt

MU = 398600  # Gravitational parameter for Earth in km^3/s^2

def getOrbitalElements(position, velocity):
    """
    Calculate the orbital elements from position and velocity vectors.

    Parameters:
    position (numpy.ndarray): Position vector in km.
    velocity (numpy.ndarray): Velocity vector in km/s.

    Returns:
    tuple: Semi-major axis (a), eccentricity (e), inclination (i), right ascension of ascending node (RAAN), argument of periapsis (w), true anomaly (v).
    """
    # Constants
   
    # Calculate specific angular momentum
    angularMomentum = np.cross(position, velocity)
    angularMomentumMagnitude = np.linalg.norm(angularMomentum)

    # Calculate semi-major axis
    #Paso a arrays
    position = np.asarray(position)
    velocity = np.asarray(velocity)
    radius = np.linalg.norm(position)
    
    semiMajorAxis = 1 / ((2 / radius) - (velocity**2 / MU))

    # Calculate eccentricity vector
    eccentricityVector = (np.cross(velocity, angularMomentum) / MU) - (position / radius)
    e     = np.linalg.norm(eccentricityVector)

    # Calculate inclination
    i = np.arccos(angularMomentum[2] / angularMomentumMagnitude)

    # Calculate right ascension of ascending node (RAAN)
    RAAN = np.arctan2(angularMomentum[0], -angularMomentum[1])

    # Calculate argument of periapsis (w)
    w = np.arctan2(eccentricityVector[2] / np.sin(i), eccentricityVector[0] * np.cos(RAAN) + eccentricityVector[1] * np.sin(RAAN))

    # Calculate true anomaly (v)
    p = angularMomentum**2 / MU  # semi-latus rectum
    senTrueAnomaly = ( p /radius ) * np.dot(position, velocity) / np.sqrt(angularMomentum**2)
    cosTrueAnomaly = (p / radius ) - 1
    trueAnomaly = np.arctan2(senTrueAnomaly, cosTrueAnomaly)

    print(f"Position: {position}, Velocity: {velocity}")
    print(f"Orbital Elements: a={semiMajorAxis}, e={e}, i={i}, RAAN={RAAN}, w={w}, v={trueAnomaly}")

    return semiMajorAxis, e, i, RAAN, w, trueAnomaly