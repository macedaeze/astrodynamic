import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Ej2_8 import getMeanAnomalyFromTrue
from Ej2_6 import getTrueAnomaly
import unittest

# Constante gravitacional para la Tierra en km^3/s^2
MU = 398600.0

def calculateOrbitalElements(position, velocity):
    """
    Calcular los elementos orbitales a partir de vectores de posición y velocidad.
    
    Parameters:
    position (numpy.ndarray): Vector de posición [x, y, z] en km
    velocity (numpy.ndarray): Vector de velocidad [vx, vy, vz] en km/s
    
    Returns:
    dict: Diccionario con los elementos orbitales (a, e, i, raan, argPeri, trueAnomaly)
    """
    # Asegurar que son arrays de numpy
    position = np.asarray(position)
    velocity = np.asarray(velocity)
    
    # Magnitudes de posición y velocidad
    positionMag = np.linalg.norm(position)
    velocityMag = np.linalg.norm(velocity)
    
    # Momento angular específico --> h
    angularMomentum = np.cross(position, velocity)
    angularMomentumMag = np.linalg.norm(angularMomentum)
    
    # Vector de excentricidad
    eccentricityVector = np.cross(velocity, angularMomentum) / MU - position / positionMag
    eccentricity = np.linalg.norm(eccentricityVector)
    
    # Energía específica
    specificEnergy = velocityMag**2 / 2 - MU / positionMag
    
    # Semieje mayor
    semiMajorAxis = -MU / (2 * specificEnergy)
    
    # Inclinación
    inclination = np.arccos(angularMomentum[2] / angularMomentumMag)
    
    # Vector de nodo ascendente
    nodeVector = np.cross([0, 0, 1], angularMomentum)
    nodeMag = np.linalg.norm(nodeVector)
    
    # RAAN (Ascensión recta del nodo ascendente)
    if nodeMag < 1e-10:  # Órbita ecuatorial
        raan = 0.0
    else:
        raan = np.arccos(nodeVector[0] / nodeMag)
        if nodeVector[1] < 0:
            raan = 2 * np.pi - raan
    
    # Argumento del periapsis
    if nodeMag < 1e-10:  # Órbita ecuatorial
        argPeri = np.arctan2(eccentricityVector[1], eccentricityVector[0])
    elif eccentricity < 1e-10:  # Órbita circular
        argPeri = 0.0
    else:
        argPeri = np.arccos(np.dot(nodeVector, eccentricityVector) / (nodeMag * eccentricity))
        if eccentricityVector[2] < 0:
            argPeri = 2 * np.pi - argPeri
    
    # Anomalía verdadera
    if eccentricity < 1e-10:  # Órbita circular
        trueAnomaly = np.arccos(np.dot(position, eccentricityVector) / (positionMag * eccentricity)) if eccentricity > 0 else 0.0
        if np.dot(position, velocity) < 0:
            trueAnomaly = 2 * np.pi - trueAnomaly
    else:
        trueAnomaly = np.arccos(np.dot(eccentricityVector, position) / (eccentricity * positionMag))
        if np.dot(position, velocity) < 0:
            trueAnomaly = 2 * np.pi - trueAnomaly
    
    return {
        'a': semiMajorAxis,
        'e': eccentricity,
        'i': inclination,
        'raan': raan,
        'argPeri': argPeri,
        'trueAnomaly': trueAnomaly
    }

def kepler2state(elements, time):
    """
    Convertir elementos orbitales a vector de estado en un tiempo dado usando la ecuación de Kepler.
    
    Parameters:
    elements (dict): Elementos orbitales (a, e, i, raan, argPeri, trueAnomaly)
    time (float): Tiempo desde la época inicial en segundos
    
    Returns:
    tuple: (position, velocity) en el tiempo solicitado
    """
    # Extraer elementos orbitales
    a = elements['a']
    e = elements['e']
    i = elements['i']
    raan = elements['raan']
    argPeri = elements['argPeri']
    trueAnomaly0 = elements['trueAnomaly']

    meanAnomaly0 = getMeanAnomalyFromTrue(e, trueAnomaly0)
    
    # Calcular movimiento medio (n)
    meanMotion = np.sqrt(MU / a**3)
    
    # Calcular anomalía media en el tiempo solicitado (M)
    meanAnomaly = meanAnomaly0 + meanMotion * time
    
    # Resolver la ecuación de Kepler para obtener la anomalía excéntrica (E)
    # M = E - e * sin(E)
    # Usando método iterativo de Newton
    eccAnomaly = meanAnomaly  # Valor inicial
    for _ in range(10):  # Normalmente converge en pocas iteraciones
        eccAnomaly = eccAnomaly - (eccAnomaly - e * np.sin(eccAnomaly) - meanAnomaly) / (1 - e * np.cos(eccAnomaly))
    
    # Calcular anomalía verdadera desde anomalía excéntrica
    # tan(f/2) = sqrt((1+e)/(1-e)) * tan(E/2)
    trueAnomaly = getTrueAnomaly(e, eccAnomaly)

    # Calcular distancia al foco (r)
    radius = a * (1 - e * np.cos(eccAnomaly))
    
    # Calcular posición en el plano orbital
    xOrbit = radius * np.cos(trueAnomaly)
    yOrbit = radius * np.sin(trueAnomaly)
    
    # Calcular velocidad en el plano orbital
    p = a * (1 - e**2)  # Semilatus rectum
    factor = np.sqrt(MU / p)
    vxOrbit = -factor * np.sin(trueAnomaly)
    vyOrbit = factor * (e + np.cos(trueAnomaly))
    
    # Matrices de rotación
    # Rotación alrededor del eje z por el argumento del periapsis
    R3_w = np.array([
        [np.cos(argPeri), -np.sin(argPeri), 0],
        [np.sin(argPeri), np.cos(argPeri), 0],
        [0, 0, 1]
    ])
    
    # Rotación alrededor del eje x por la inclinación
    R1_i = np.array([
        [1, 0, 0],
        [0, np.cos(i), -np.sin(i)],
        [0, np.sin(i), np.cos(i)]
    ])
    
    # Rotación alrededor del eje z por el RAAN
    R3_raan = np.array([
        [np.cos(raan), -np.sin(raan), 0],
        [np.sin(raan), np.cos(raan), 0],
        [0, 0, 1]
    ])
    
    # Matriz de transformación completa
    transformMatrix = R3_raan @ R1_i @ R3_w
    
    # Posición en el plano orbital transformada al sistema de referencia inercial
    position = transformMatrix @ np.array([xOrbit, yOrbit, 0])
    
    # Velocidad en el plano orbital transformada al sistema de referencia inercial
    velocity = transformMatrix @ np.array([vxOrbit, vyOrbit, 0])
    
    return position, velocity

def propagateOrbit(position0, velocity0, timeSpan, numPoints=100):
    """
    Propagar una órbita elíptica usando la ecuación de Kepler.
    
    Parameters:
    position0 (numpy.ndarray): Vector de posición inicial [x, y, z] en km
    velocity0 (numpy.ndarray): Vector de velocidad inicial [vx, vy, vz] en km/s
    timeSpan (tuple): Intervalo de tiempo [tiempoInicial, tiempoFinal] en segundos
    numPoints (int): Número de puntos para la propagación
    
    Returns:
    numpy.ndarray: Matriz 6xN con vectores de estado para cada tiempo
    numpy.ndarray: Vector de tiempos
    """
    # Calcular elementos orbitales
    elements = calculateOrbitalElements(position0, velocity0)
    
    # Verificar que la órbita es elíptica
    if elements['e'] >= 1.0:
        raise ValueError("Este simulador solo funciona para órbitas elípticas (e < 1)")
    
    # Crear vector de tiempos
    times = np.linspace(timeSpan[0], timeSpan[1], numPoints)
    
    # Inicializar matriz de estados (posición y velocidad)
    states = np.zeros((6, numPoints))
    
    # Propagar la órbita para cada tiempo
    for i, t in enumerate(times):
        position, velocity = kepler2state(elements, t)
        states[0:3, i] = position
        states[3:6, i] = velocity
    
    return states, times

def plotOrbit3D(states, centralBodyRadius=6371.0):
    """
    Visualizar la órbita en 3D.
    
    Parameters:
    states (numpy.ndarray): Matriz 6xN con vectores de estado
    centralBodyRadius (float): Radio del cuerpo central en km
    """
    # Crear la figura y el eje 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Extraer las coordenadas
    x = states[0, :]
    y = states[1, :]
    z = states[2, :]
    
    # Dibujar la órbita
    ax.plot(x, y, z, 'b-', label='Órbita')
    
    # Marcar posición inicial
    ax.plot([x[0]], [y[0]], [z[0]], 'go', label='Inicio')
    
    # Configuración del gráfico
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title('Trayectoria Orbital Elíptica')
    ax.legend()
    
    # Ajustar los límites para una mejor visualización
    maxRange = np.max([np.max(np.abs(x)), np.max(np.abs(y)), np.max(np.abs(z))])
    ax.set_xlim([-maxRange, maxRange])
    ax.set_ylim([-maxRange, maxRange])
    ax.set_zlim([-maxRange, maxRange])
    
    plt.grid(True)
    plt.tight_layout()
    
    return fig, ax

def runSimulation(position0, velocity0, timeSpan, numPoints=100):
    """
    Ejecuta la simulación del problema de dos cuerpos para órbitas elípticas.
    
    Parameters:
    position0 (numpy.ndarray): Vector de posición inicial [x, y, z] en km
    velocity0 (numpy.ndarray): Vector de velocidad inicial [vx, vy, vz] en km/s
    timeSpan (tuple): Intervalo de tiempo [tiempoInicial, tiempoFinal] en segundos
    numPoints (int): Número de puntos para la propagación
    
    Returns:
    tuple: (estados, tiempos, elementos_orbitales)
    """
    # Calcular elementos orbitales iniciales
    orbitalElements = calculateOrbitalElements(position0, velocity0)
    
    # Verificar que la órbita es elíptica
    if orbitalElements['e'] >= 1.0:
        raise ValueError("Este simulador solo funciona para órbitas elípticas (e < 1)")
    
    # Propagar la órbita
    states, times = propagateOrbit(position0, velocity0, timeSpan, numPoints)
    
    # Visualizar la órbita
    plotOrbit3D(states)
    plt.show()
    
    return states, times, orbitalElements

class TestOrbitalMechanics(unittest.TestCase):
    
    def setUp(self):
        """
        Configuración inicial para las pruebas.
        Define una órbita de prueba común.
        """
        # Configuración de una órbita circular ecuatorial a 500 km de altura
        self.earthRadius = 6371.0  # km
        self.altitude = 500.0  # km
        self.radius = self.earthRadius + self.altitude
        
        # Velocidad circular
        self.velocity_circ = np.sqrt(MU / self.radius)
        
        # Posición y velocidad iniciales para órbita circular
        self.position_circ = np.array([self.radius, 0.0, 0.0])  # km
        self.velocity_circ_vec = np.array([0.0, self.velocity_circ, 0.0])  # km/s
        
        # Órbita elíptica (e = 0.1)
        self.e = 0.1
        self.a = self.radius / (1 - self.e)  # km (perigeo en self.radius)
        self.velocity_ellip = np.sqrt(MU * (2/self.radius - 1/self.a))  # km/s
        self.position_ellip = np.array([self.radius, 0.0, 0.0])  # km
        self.velocity_ellip_vec = np.array([0.0, self.velocity_ellip, 0.0])  # km/s
        
        # Órbita inclinada
        self.inclination = np.radians(45.0)  # 45 grados
        self.velocity_incl = np.array([
            0.0, 
            self.velocity_circ * np.cos(self.inclination), 
            self.velocity_circ * np.sin(self.inclination)
        ])
    
    
    def test_calculate_orbital_elements_elliptical(self):
        """Prueba el cálculo de elementos orbitales para una órbita elíptica."""
        elements = calculateOrbitalElements(self.position_ellip, self.velocity_ellip_vec)
        
        self.assertAlmostEqual(elements['a'], self.a, delta=1e-6)
        self.assertAlmostEqual(elements['e'], self.e, delta=1e-2)
        self.assertAlmostEqual(elements['i'], 0.0, delta=1e-6)
        self.assertAlmostEqual(elements['trueAnomaly'], 0.0, delta=1e-6)
    
    
    def test_kepler_state_conversion_roundtrip(self):
        """
        Prueba la conversión de estado a elementos orbitales y de vuelta a estado.
        Comprueba que el resultado del roundtrip es el mismo que el original.
        """
        # Calcular elementos orbitales
        elements = calculateOrbitalElements(self.position_ellip, self.velocity_ellip_vec)
        
        # Convertir elementos orbitales de vuelta a estado (en t=0)
        position, velocity = kepler2state(elements, 0)
        
        # Verificar que la posición y velocidad son aproximadamente las mismas
        np.testing.assert_allclose(position, self.position_ellip, rtol=1e-5)
        np.testing.assert_allclose(velocity, self.velocity_ellip_vec, rtol=1e-5)
    
    def test_propagate_orbit_period(self):
        """
        Prueba que después de un período orbital, la posición es aproximadamente la misma.
        """
        # Calcular elementos orbitales
        elements = calculateOrbitalElements(self.position_ellip, self.velocity_ellip_vec)
        
        # Calcular período orbital
        period = 2 * np.pi * np.sqrt(elements['a']**3 / MU)
        
        # Propagar por un período
        states, times = propagateOrbit(self.position_ellip, self.velocity_ellip_vec, (0, period), 100)
        
        # Verificar que la posición final es aproximadamente igual a la inicial
        np.testing.assert_allclose(states[0:3, 0], states[0:3, -1], rtol=1e-3, atol=1e-8)
    

if __name__ == '__main__':
    
    position0 = np.array([7000.0, 0.0, 0.0])   # km
    velocity0 = np.array([0.0, 7.5, 2.0])      # km/s
    timeSpan = (0, 15000)                  # segundos

    runSimulation(position0, velocity0, timeSpan)

    unittest.main()