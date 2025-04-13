import math

# Ejercicio 1.7
# Escribir dos funciones en Python: ae2Eh() que a partir del semi-eje mayor y la excentricidad calcule la energía específica y el
# módulo del momento angular y Eh2ae que resuelva el problema inverso. 

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

#SINGULARIDADES
#Supongo con sigularidades que se refieren a casos especiales pero no debemos incluir los casos fisicamente imposibles como e<0 o a=0
#Si E=0 entonces a->infinito pero daria error la division por 0, por lo tanto hay que poner una condicion que atrape este caso (Parabolica)
#  Si e=1 tambien daria error ya que daria h=0 cuando tampoco es cierto. Ponemos otra condicion


def main():

    print("Seleccione la transformación:")
    print("1) (a, e) -> (ε, h)")
    print("2) (ε, h) -> (a, e)")
    choice = input("Ingrese 1 o 2: ").strip()
  
    if choice == "1":
        print("\nIngrese los datos para el semieje mayor y la exentricidad:")
        a = float(input("  a [m]: "))
        e = float(input("  e: "))
        try:
            (energia, h) = ae2Eh(a, e)
            print(f"\nResultados:")
            print(f"  ε (energía específica) = {energia:.2g} J/kg") #Con el .2g se limita a 2 cifras significativas
            print(f"  h (momento angular específico) = {h:.2g} m^2/s")
        except ValueError as err:
            print(f"Error: {err}")
        
    elif choice == "2":
        print("\nIngrese los datos para Energia y Momento Angular:")
        energia = float(input("  ε (J/kg): "))
        h = float(input("  h (m^2/s): "))
        
        try:
            (a, e) = Eh2ae(energia, h)
            print(f"\nResultados:")
            print(f"  a (semieje mayor) = {a:.2g} m")
            print(f"  e (exentricidad) = {e:.2g}")
        except ValueError as err:
            print(f"Error: {err}")
        a, e = Eh2ae(energia, h, mu)

    
    else:
        print("Opción no válida. Saliendo...")

if __name__ == "__main__":
    main()