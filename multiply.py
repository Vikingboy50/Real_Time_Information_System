#------------------------------------------
# Name:         multiply.py
# Description:  Final assignment for Real Time Information Systems
# Author:       LAVIGNE LUCAS
#------------------------------------------

import time
import numpy as np
import matplotlib.pyplot as plt
import random 

def multiply():
    """Multipliy 2 randomly generated number and gives the execution time of the operation
    Returns:
        float: the execution time of the multiplication
    """
    start_time = time.time()
    a = random.randint(1, 1000000000)
    b = random.randint(1, 1000000000)
    result = a * b
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time

if __name__ == "__main__":
    execution_times = []
    for i in range(100000):
        execution_times.append(multiply())
    
    print("Stats:")
    print(f"Min execution time: {min(execution_times)} seconds")
    print(f"Max execution time: {max(execution_times)} seconds")
    print(f"Q1 execution time: {np.percentile(execution_times, 25)} seconds")
    print(f"Q2 execution time: {np.percentile(execution_times, 50)} seconds")
    print(f"Q3 execution time: {np.percentile(execution_times, 75)} seconds")
        
    #plot the histogram of execution times
    plt.hist(execution_times)
    plt.title("Execution Time of Multiplication")
    plt.xlabel("Execution Time (seconds)")
    plt.ylabel("Frequency")
    plt.show()
    
    