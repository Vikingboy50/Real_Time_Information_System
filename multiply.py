#------------------------------------------
# Name:         multiply.py
# Description:  Final assignment for Real Time Information Systems
# Author:       LAVIGNE LUCAS
#------------------------------------------

import time
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import itertools

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
    #plt.show()
    
    #----------------------------------
    # Determination du planning optimal
    #----------------------------------
    
    # Task parameters
    Tasks = [
        {"name": "Task 1", "execution_time": 3, "period": 10},
        {"name": "Task 2", "execution_time": 3, "period": 10},
        {"name": "Task 3", "execution_time": 2, "period": 20},
        #On limite le nombre de tâches pour éviter une explosion combinatoire du nombre de plannings possibles
        #{"name": "Task 4", "execution_time": 2, "period": 20},
        #{"name": "Task 5", "execution_time": 2, "period": 40},
        #{"name": "Task 6", "execution_time": 2, "period": 40},
        #{"name": "Task 7", "execution_time": 3, "period": 80}
    ]
    # Calculate utilization for each task
    for task in Tasks:
        task["utilization"] = task["execution_time"] / task["period"]
    #Total utilization
    total_utilization = sum(task["utilization"] for task in Tasks)
    print(f"Total Utilization: {total_utilization:.2f}")
    
    # Defining all possible schedules
    task_schedules_list = []
    
    for task in Tasks:
        for i in range(task["period"] // task["execution_time"]):
            task_schedules_list.append({
                "name": task["name"],
                "execution_time": task["execution_time"],
                "period": task["period"],
                "instance": i + 1
            })
    print("Task schedules list:")
    for task in task_schedules_list:
        print(task)
    
    # Pré-calcul des informations pour l'algorithme de génération de plannings avec algo de backtracking
    task_counts = {task["name"]: task["period"] // task["execution_time"] for task in Tasks} # Nombre d'instances de chaque tâche
    task_instances_map = {task["name"]: [] for task in Tasks} # Map pour stocker les instances de chaque tâche
    for instance in task_schedules_list:
        task_instances_map[instance["name"]].append(instance)# On remplit la map avec les instances de chaque tâche
        
    all_possible_schedules = []
    
    def generate_schedules(current_schedule, counts):
        """Génère tous les plannings possibles en utilisant un algorithme de backtracking.
        current_schedule: le planning en cours de construction
        counts: un dictionnaire qui suit le nombre d'instances de chaque tâche déjà utilisées dans le planning en cours de construction
        """
        if len(current_schedule) == len(task_schedules_list):
            all_possible_schedules.append(list(current_schedule))
            return
            
        for task in Tasks:
            name = task["name"]
            if counts[name] < task_counts[name]: # Si on n'a pas encore utilisé toutes les instances de cette tâche
                current_schedule.append(task_instances_map[name][counts[name]]) # On ajoute la prochaine instance de cette tâche au planning en cours de construction
                counts[name] += 1
                generate_schedules(current_schedule, counts) # On continue à construire le planning avec cette instance de tâche ajoutée
                counts[name] -= 1
                current_schedule.pop() # On retire la tâche ajoutée pour essayer une autre instance de tâche ou une autre tâche

    generate_schedules([], {task["name"]: 0 for task in Tasks})
    
    print(f"Number of possible schedules: {len(all_possible_schedules)}")
    
    # Computation of response times for each schedule
    def compute_response_times(schedule):
        """Calcule les temps de réponse pour un planning donné.
        schedule: le planning pour lequel on veut calculer les temps de réponse
        """
        response_times = {}
        current_time = 0
        
        for task_instance in schedule:
            task_name = task_instance["name"]
            execution_time = task_instance["execution_time"]
            period = task_instance["period"]
            
            # Le temps de réponse est le temps actuel plus le temps d'exécution de la tâche
            response_time = current_time + execution_time
            
            # On stocke le temps de réponse pour cette instance de tâche
            response_times[(task_name, task_instance["instance"])] = response_time
            
            # On avance le temps actuel du temps d'exécution de la tâche
            current_time += execution_time
            
            # Si le temps actuel dépasse la période de la tâche, cela signifie que la tâche n'est pas terminée avant sa prochaine instance, donc on peut arrêter le calcul des temps de réponse pour ce planning
            if current_time > period:
                return None
        
        return response_times
    
    optimal_schedule = None
    optimal_response_times = None
    
    for schedule in all_possible_schedules:
        response_times = compute_response_times(schedule)
        if response_times is not None: # Si le planning est réalisable (tous les temps de réponse sont inférieurs aux périodes correspondantes)
            if optimal_response_times is None or max(response_times.values()) < max(optimal_response_times.values()):
                optimal_schedule = schedule
                optimal_response_times = response_times
    
    print("Optimal Schedule:")
    for task_instance in optimal_schedule:
        print(task_instance)
    print("Optimal Response Times:")
    for task_instance, response_time in optimal_response_times.items():
        print(f"{task_instance}: {response_time} ms")
    