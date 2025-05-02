import numpy as np
import matplotlib.pyplot as plt
from Ej2_8 import getMeanAnomalyFromTrue

def plotMeanVsTrueAnomaly():

    """
    Funcion que grafica la anomalia media en funcion de la anomalia verdadera para 10 valores distintos de excentricidad.

    No tiene parametros y no retorna nada
    """
     # Definimos los valores de ecentricidad y anomalia verdadera
    eccentricityVal = np.linspace(0, 0.99, 10)
    TrueAnomalyDegVal = np.arange(-180, 181, 10)  # de -180 a 180 grados

    plt.figure(figsize=(7, 7))

    # Iteramos sobre los valores de ecentricidad
    for e in eccentricityVal:
        # Convertimos trueAnomaly a radianes
        TrueAnomalyRadVal = np.radians(TrueAnomalyDegVal)
   
        if e == 0.0:
            meanAnomalyDegVal = TrueAnomalyDegVal
        else:
            meanAnomalyRadVal = getMeanAnomalyFromTrue(e, TrueAnomalyRadVal)
             # Convertimos M a grados
            meanAnomalyDegVal = np.degrees(meanAnomalyRadVal)

        # Graficamos: E (°) vs. v (°)
        plt.plot(TrueAnomalyDegVal, meanAnomalyDegVal, label=f'e={e:.2f}')

    # Configuramos el grafico
    plt.title("Mean Anomaly (M) vs. True Anomaly (v) for 10 e in [0, 0.99]")
    plt.xlabel("True Anomaly v (°)")
    plt.ylabel("Mean Anomaly M (°)")
    plt.xlim(-180, 180)
    plt.ylim(-180, 180)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.axvline(0, color='black', linewidth=0.8)
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    
    plotMeanVsTrueAnomaly()


