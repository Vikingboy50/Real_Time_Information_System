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

print("Compiling...")
subprocess.run(["gcc", "multiply.c", "-o", "multiply.exe"])

execution_times = []
iterations = 1000
print(f"Calculating {iterations} multiplications...")
for i in range(iterations):
    start_time = time.perf_counter()
    subprocess.run(["./multiply.exe"], capture_output=True, text=True)
    end_time = time.perf_counter()
    execution_times.append((end_time - start_time) * 1e3)  # Convert to milliseconds
    print(f"Execution percentage: {((i+1)/iterations)*100:.2f}%", end="\r")

print("Stats:")
print(f"Min execution time: {min(execution_times)} milliseconds")
print(f"Max execution time: {max(execution_times)} milliseconds")
print(f"Q1 execution time: {np.percentile(execution_times, 25)} milliseconds")
print(f"Q2 execution time: {np.percentile(execution_times, 50)} milliseconds")
print(f"Q3 execution time: {np.percentile(execution_times, 75)} milliseconds")
print(f"WCET execution time: {max(execution_times)} milliseconds")
    
# We limit the interval to the 99th percentile to ignore the rare extreme values (outliers)
upper_bound = np.percentile(execution_times, 99)

# Plot the histogram of execution times with more bars (bins) and a reduced interval (range)
plt.hist(execution_times, bins=50, range=(min(execution_times), upper_bound), color='skyblue', edgecolor='black')
plt.title("Execution Time of Multiplication")
plt.xlabel("Execution Time (milliseconds)")
plt.ylabel("Frequency")
#plt.show()

#%%

import numpy as np
import math

# ==========================================
# 1. Task Set Configuration
# ==========================================
# Format: { "id": "t_name", "C": execution_time, "T": period }
# We assume that Deadline (D) = Period (T)
tasks = [
    {"id": "t1", "C": 3, "T": 10},
    {"id": "t2", "C": 3, "T": 10},
    {"id": "t3", "C": 2, "T": 20},
    {"id": "t4", "C": 2, "T": 20},
    {"id": "t5", "C": 2, "T": 40},
    {"id": "t6", "C": 2, "T": 40},
    {"id": "t7", "C": 3, "T": 80},
]

# Calculation of the hyperperiod (LCM of periods)
periods = [t["T"] for t in tasks]
hyperperiod = math.lcm(*periods)

# Calculation of processor utilization (U)
utilization = sum(t["C"] / t["T"] for t in tasks)

# ==========================================
# 2. Non-Preemptive Scheduling (EDF)
# ==========================================
def generate_schedule(tasks, hyperperiod):
    jobs = []
    # Generation of all jobs over the hyperperiod
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
        # Available jobs at time t
        available_jobs = [j for j in jobs if j["arrival"] <= current_time and j["start_time"] is None]
        
        if not available_jobs:
            current_time += 1
            idle_times += 1
            continue
        available_jobs.sort(key=lambda x: (x["deadline"], x["execution"]))
        
        selected_job = available_jobs[0]
        selected_job["start_time"] = current_time
        selected_job["end_time"] = current_time + selected_job["execution"]
        
        # The processor is busy until the end of the job (Non-preemptive)
        current_time = selected_job["end_time"]
        completed_jobs.append(selected_job)

    return completed_jobs, idle_times

# ==========================================
# 3. Execution and Verification
# ==========================================
print(f"\n--- Basic Analysis ---")
print(f"Hyperperiod (H): {hyperperiod}")
print(f"Utilization (U) with C1={3}: {utilization:.4f} (Must be <= 1 to be schedulable)")

schedule, total_idle_time = generate_schedule(tasks, hyperperiod)

missed_deadlines = []
total_wait_time = 0

print("\n--- Response time analysis (per job) ---")
for job in sorted(schedule, key=lambda x: x["start_time"]):
    response_time = job["end_time"] - job["arrival"]
    wait_time = job["start_time"] - job["arrival"]
    total_wait_time += wait_time
    
    status = "OK"
    if response_time > (job["deadline"] - job["arrival"]):
        status = "MISSED DEADLINE"
        missed_deadlines.append(job)
        
    print(f"[{job['start_time']:02d}-{job['end_time']:02d}] {job['job_id']:<6} | Arrival: {job['arrival']:02d} | Deadline: {job['deadline']:02d} | Resp: {response_time:02d} | Wait: {wait_time:02d} -> {status}")

print("\n--- Optimization Summary ---")
print(f"Total waiting time (Delay) : {total_wait_time}")
print(f"Total processor idle time : {total_idle_time}")

# Verification of the paradox mentioned in the statement
expected_idle_time = hyperperiod - sum(t["C"] * (hyperperiod // t["T"]) for t in tasks)
print(f"Verification : The theoretical total idle time over the hyperperiod is {expected_idle_time}.")
if total_idle_time == expected_idle_time:
    print("Conclusion : Minimizing the waiting time modifies the *timing* of the idle time, but the *total* idle time over the hyperperiod remains constant and depends solely on the Task Set characteristics.")
    
# %%
