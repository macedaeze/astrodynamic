# En este archivo se encuentra la funcion getMeanAnomaly que calcula la anomalia media a partir de la excentricidad y la anomalia excentrica.

import matplotlib.pyplot as plt
import numpy as np

def getMeanAnomaly(eccentricity, eccentricAnomaly):
    """
    Funcion que calcula la anomalia media a partir de la excentricidad y la anomalia excentrica.
    
    Parametros:
    e (float): Exentricidad [adimensional]
    E (float): Anomalia excentrica [en radianes]
    
    Retorna:
    float: Anomalia media [en radianes]
    """
    
    # Inicializamos la anomalia media
    meanAnomaly = eccentricAnomaly - eccentricity * np.sin(eccentricAnomaly)
    
    return meanAnomaly

def plotMeanVsEccentricAnomaly():
    """
    Funcion que grafica la anomalia media en funcion de la anomalia excentrica para 10 valores distintos de excentricidad.

    No tiene parametros y no retorna nada
    
    """

    # Definimos los valores de ecentricidad y anomalia media
    eccentricityVal = np.linspace(0, 0.99, 10)
    eccentricAnomalyDegVal = np.arange(-180, 181, 10)  # de -180 a 180 grados

    plt.figure(figsize=(7, 7))

    # Iteramos sobre los valores de ecentricidad
    for e in eccentricityVal:
        # Convertimos E a radianes
        eccentricAnomalyRadVal = np.radians(eccentricAnomalyDegVal)
        
        # Ecuación de Kepler (en rad): M = E - e*sin(E)
        meanAnomalyRadVal = getMeanAnomaly(e, eccentricAnomalyRadVal)

        # Convertimos M a grados
        meanAnomalyDegVal = np.degrees(meanAnomalyRadVal)

        # Graficamos: E (°) vs. M (°)
        plt.plot(eccentricAnomalyDegVal, meanAnomalyDegVal, label=f'e={e:.2f}')



    # Configuramos el grafico
    plt.title("Mean Anomaly (M) vs. Eccentric Anomaly (E) for 10 e in [0, 0.99]")
    plt.xlabel("Eccentric Anomaly E (°)")
    plt.ylabel("Mean Anomaly M (°)")
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    
    plotMeanVsEccentricAnomaly()