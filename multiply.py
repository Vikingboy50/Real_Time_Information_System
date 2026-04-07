#------------------------------------------
# Name:         multiply.py
# Description:  Final assignment for Real Time Information Systems
# Author:       LAVIGNE LUCAS
#------------------------------------------

import time
import subprocess
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("Compilation en cours...")
    subprocess.run(["gcc", "multiply.c", "-o", "multiply.exe"])
    
    execution_times = []
    iterations = 1000
    print(f"Calcul de {iterations} multiplications...")
    for i in range(iterations):
        start_time = time.perf_counter()
        subprocess.run(["./multiply.exe"], capture_output=True, text=True)
        end_time = time.perf_counter()
        execution_times.append((end_time - start_time) * 1e3)  # Convert to milliseconds
        print(f"Pourcentage d'exécution: {((i+1)/iterations)*100:.2f}%", end="\r")
    
    print("Stats:")
    print(f"Min execution time: {min(execution_times)} milliseconds")
    print(f"Max execution time: {max(execution_times)} milliseconds")
    print(f"Q1 execution time: {np.percentile(execution_times, 25)} milliseconds")
    print(f"Q2 execution time: {np.percentile(execution_times, 50)} milliseconds")
    print(f"Q3 execution time: {np.percentile(execution_times, 75)} milliseconds")
    print(f"WCET execution time: {max(execution_times)} milliseconds")
        
    # On limite l'intervalle au 99e centile pour ignorer les rares valeurs extrêmes (outliers)
    upper_bound = np.percentile(execution_times, 99)
    
    # plot the histogram of execution times avec plus de barres (bins) et un intervalle réduit (range)
    plt.hist(execution_times, bins=50, range=(min(execution_times), upper_bound), color='skyblue', edgecolor='black')
    plt.title("Execution Time of Multiplication")
    plt.xlabel("Execution Time (milliseconds)")
    plt.ylabel("Frequency")
    plt.show()
    
    