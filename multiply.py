#------------------------------------------
# Name:         multiply.py
# Description:  Final assignment for Real Time Information Systems
# Author:       LAVIGNE LUCAS
#------------------------------------------

import time
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import math

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

#%%

import numpy as np
import math

# ==========================================
# 1. Configuration du Task Set
# ==========================================
# Format: { "id": "t_name", "C": execution_time, "T": period }
# On assume que Deadline (D) = Period (T)
tasks = [
    {"id": "t1", "C": 3, "T": 10},
    {"id": "t2", "C": 3, "T": 10},
    {"id": "t3", "C": 2, "T": 20},
    {"id": "t4", "C": 2, "T": 20},
    {"id": "t5", "C": 2, "T": 40},
    {"id": "t6", "C": 2, "T": 40},
    {"id": "t7", "C": 3, "T": 80},
]

# Calcul de l'hyperpériode (PPCM des périodes)
periods = [t["T"] for t in tasks]
hyperperiod = math.lcm(*periods)

# Calcul de l'utilisation du processeur (U)
utilization = sum(t["C"] / t["T"] for t in tasks)

# ==========================================
# 2. Ordonnancement Non-Préemptif (EDF)
# ==========================================
def generate_schedule(tasks, hyperperiod):
    jobs = []
    # Génération de tous les jobs sur l'hyperpériode
    for t in tasks:
        num_jobs = hyperperiod // t["T"]
        for k in range(num_jobs):
            jobs.append({
                "task_id": t["id"],
                "job_id": f"{t['id']}_{k+1}",
                "arrival": k * t["T"],
                "execution": t["C"],
                "deadline": (k + 1) * t["T"],
                "start_time": None,
                "end_time": None
            })
            
    current_time = 0
    completed_jobs = []
    idle_times = 0
    
    while len(completed_jobs) < len(jobs):
        # Jobs disponibles à l'instant t
        available_jobs = [j for j in jobs if j["arrival"] <= current_time and j["start_time"] is None]
        
        if not available_jobs:
            current_time += 1
            idle_times += 1
            continue
            
        # Stratégie EDF (Earliest Deadline First) pour minimiser l'attente tout en respectant les échéances
        # En cas d'égalité d'échéance, on favorise le temps d'exécution le plus court (SJF)
        available_jobs.sort(key=lambda x: (x["deadline"], x["execution"]))
        
        selected_job = available_jobs[0]
        selected_job["start_time"] = current_time
        selected_job["end_time"] = current_time + selected_job["execution"]
        
        # Le processeur est occupé jusqu'à la fin du job (Non-préemptif)
        current_time = selected_job["end_time"]
        completed_jobs.append(selected_job)

    return completed_jobs, idle_times

# ==========================================
# 3. Exécution et Vérification
# ==========================================
print(f"\n--- Analyse de base ---")
print(f"Hyperpériode (H): {hyperperiod}")
print(f"Utilisation (U) avec C1={3}: {utilization:.4f} (Doit être <= 1 pour être ordonnançable)")

schedule, total_idle_time = generate_schedule(tasks, hyperperiod)

missed_deadlines = []
total_wait_time = 0

print("\n--- Analyse des temps de réponse (par job) ---")
for job in sorted(schedule, key=lambda x: x["start_time"]):
    response_time = job["end_time"] - job["arrival"]
    wait_time = job["start_time"] - job["arrival"]
    total_wait_time += wait_time
    
    status = "OK"
    if response_time > (job["deadline"] - job["arrival"]):
        status = "MISSED DEADLINE"
        missed_deadlines.append(job)
        
    print(f"[{job['start_time']:02d}-{job['end_time']:02d}] {job['job_id']:<6} | Arrivée: {job['arrival']:02d} | Échéance: {job['deadline']:02d} | Rép: {response_time:02d} | Attente: {wait_time:02d} -> {status}")

print("\n--- Bilan de l'optimisation ---")
print(f"Temps d'attente total (Délai) : {total_wait_time}")
print(f"Temps d'inactivité total du processeur : {total_idle_time}")

# Vérification du paradoxe mentionné dans l'énoncé
expected_idle_time = hyperperiod - sum(t["C"] * (hyperperiod // t["T"]) for t in tasks)
print(f"Vérification : Le temps d'inactivité total théorique sur l'hyperpériode est de {expected_idle_time}.")
if total_idle_time == expected_idle_time:
    print("Conclusion : Minimiser le temps d'attente modifie le *moment* de l'inactivité, mais l'inactivité *totale* sur l'hyperpériode reste constante et dépend uniquement des caractéristiques du Task Set.")
    
# %%
