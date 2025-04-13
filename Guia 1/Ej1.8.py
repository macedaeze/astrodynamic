import math
import matplotlib.pyplot as plt
import numpy as np

# Ejercicio 1.8
# Escribir en Python una función que reciba dos parámetros (semi-eje mayor y excentricidad, O energía específica y momento angular según prefiera el 
# usuario) y dibuje una cónica en el plano.

# Constantes
G = 6.67430e-11  # Constante de gravitación universal en m^3 kg^-1 s^-2
M = 5.972e24     # Masa de la Tierra en kg
MU = G * M  # Producto de la constante de gravitación y la masa de la Tierra

def ae2Eh(a, e):
    """
    Función que calcula la energía específica y el módulo del momento angular a partir del semi-eje mayor y la excentricidad.
    
    Parámetros:
    a (float): Semi-eje mayor [en metros]
    e (float): Excentricidad [adimensional]
    
    Retorna:
    tupla: Energía específica y módulo del momento angular
    """

    # Cálculo de la energía específica de la orbita
    energia = -MU / (2 * a)

    # Cálculo del módulo del momento angular
    if e == 1:
        raise ValueError("Si la excentricidad es 0 entonces no podemos usarla para calcular el momento angular, deberiamos usar la velocidad y el radio.")
    h = math.sqrt(MU * a * (1 - e**2))

    return energia, h


def Eh2ae(energia, h):
    """
    Función que calcula el semi-eje mayor y la excentricidad a partir de la energía específica y el módulo del momento angular.
    
    Parámetros:
    E (float): Energía específica [en J/kg]
    h (float): Módulo del momento angular [en m^2/s]
    
    Retorna:
    tupla: Semi-eje mayor y excentricidad
    """

    # Cálculo del semi-eje mayor
    if energia == 0:
        raise ValueError("Si la energia es cero entonces el semi-eje mayor es infinito (parabólica), no podemos calcularlo.")
    a = -MU / (2 * energia)

    # Cálculo de la excentricidad
    e = math.sqrt(1 - (h**2 / (MU * a)))

    return a, e

#getPandTheta = lambda a, e: (a * (1 - e**2), math.acos(e)) #Función que devuelve el semieje menor y el ángulo theta

def getPandTheta(a=None, e=None, energia=None, h=None):
    """
    Función que calcula el parametro p y el vector de ángulos theta necesarios para graficar la conica
    a partir del semi-eje mayor y excentricidad o energía específica y momento angular.
    
    Parámetros:
    a (float): Semi-eje mayor [en metros]
    e (float): Excentricidad [adimensional]
    E (float): Energía específica [en J/kg]
    h (float): Módulo del momento angular [en m^2/s]
    
    Retorna:
    tupla: P y angulo theta
    """
   
    pointNumber = 500  # Número de puntos a tener en cuento al graficar la conica

    if a is None or e is None:
        a, e = Eh2ae(energia, h)
#   No es necesario calcular la energia y el momento angular, ya que no es necesario para calcular p y theta     
#    else:
#        energia, h = ae2Eh(a, e)

    # Cálculo del parámetro p y el ángulo theta
    p = a * (1 - e**2)
     # Generación del vector de ángulos theta
    if e < 1:
        # Órbita elíptica o circular: theta de 0 a 2π
        theta = np.linspace(0, 2 * np.pi, pointNumber)
    else:
        # Órbita hiperbólica: restringir rango de theta donde r(θ) > 0
        theta_max = np.arccos(-1 / e)  # límite donde denominador → 0
        theta = np.linspace(-theta_max + 1e-3, theta_max - 1e-3, pointNumber) # Uso (1e-3) para evitar la división por cero en el cálculo de r(θ)
    
    return p, e, theta


def plot_conic(p, e, theta):
    """
    Función que grafica la cónica en el plano.
    
    Parámetros:
    p (float): Parámetro de la cónica [en metros]
    e (float): Excentricidad [adimensional]
    theta (ndarray): Vector de ángulos theta [en radianes]
    """
    
    # Cálculo de las coordenadas x e y de la cónica
    r = p / (1 + e * np.cos(theta))  # Ecuación polar de la cónica
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Graficar la cónica

    plt.figure(figsize=(8, 8))
    plt.plot(x, y, label='Orbita', color='blue')
    plt.plot(0, 0, 'ro', label='Foco (cuerpo central)')
    plt.title(f"Órbita con e = {e:.2g}")
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.grid(True)
    plt.axis('equal')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


def main():

    print("Seleccione los parametros a usar para graficar la conica:")
    print("1) (a, e)")
    print("2) (ε, h)")
    choice = input("Ingrese 1 o 2: ").strip()
  
    if choice == "1":
        print("\nIngrese los datos para el semieje mayor y la exentricidad:")
        a = float(input("  a [m]: "))
        e = float(input("  e: "))
        try:
            plot_conic(*getPandTheta(a, e))
            print(f"\nResultados:")
        except ValueError as err:
            print(f"Error: {err}")
        
    elif choice == "2":
        print("\nIngrese los datos para Energia y Momento Angular:")
        epsilon = float(input("  ε (J/kg): "))
        h = float(input("  h (m^2/s): "))
        try:
            plot_conic(*getPandTheta(energia=epsilon, h=h))
            print(f"\nResultados:")
        except ValueError as err:
            print(f"Error: {err}")
        a, e = Eh2ae(epsilon, h, mu)
    else:
        print("Opción no válida. Saliendo...")

if __name__ == "__main__":
    main()