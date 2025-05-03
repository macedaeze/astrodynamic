import datetime
from sgp4.api import Satrec
import numpy as np

MU = 398600  # Gravitational parameter for Earth in km^3/s^2

# TLE (Two-Line Element) data for the satellite
TLE_LINE1 = "1 46265U 20059A   25123.17572593  .00000891  00000+0  11850-3 0  9996"
TLE_LINE2 = "2 46265  97.8893 309.9095 0001562  88.9775 271.1617 14.82145606252766"


sat = Satrec.twoline2rv(TLE_LINE1, TLE_LINE2)

# convierte JD → datetime UTC
def jd_to_datetime(satJulianDateInt, satJulianDateFrac):
    julianDateInt, julianDateFrac = sat.jdsatepoch, sat.jdsatepochF
    julianDate = julianDateInt + julianDateFrac
    J1970 = 2440587.5            # JD del 1-1-1970 00:00 UTC
    segs = (julianDate - J1970) * 86400.0
    return datetime.fromtimestamp(segs, tz=datetime.timezone.utc)

t0 = jd_to_datetime(sat.jdsatepoch, sat.jdsatepochF)

meanMotion = sat.no_kozai
orbitalPeriod = 2 * np.pi / meanMotion  # Periodo orbital en radianes
ORBIT_NUMBER = 5 #Number of orbits to propagate
STEP_MIN=1

numberOfSteps = int(orbitalPeriod * ORBIT_NUMBER / STEP_MIN) + 1 #Number of steps to propagate the orbits

times    = np.empty(numberOfSteps, dtype='datetime64[ns]')
semiMajorAxis    = np.empty(numberOfSteps)
ecentricity    = np.empty(numberOfSteps)
inclination    = np.empty(numberOfSteps)
rightAscension = np.empty(numberOfSteps)
wPeriapsis    = np.empty(numberOfSteps)
trueAnomaly   = np.empty(numberOfSteps)

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