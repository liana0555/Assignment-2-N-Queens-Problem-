import random
import math
import time
import tracemalloc

def count_conflicts(state):
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def simulated_annealing(n, max_steps=500000, start_temp=100, cooling_rate=0.995):
    state = [random.randint(0, n - 1) for _ in range(n)]
    temp = start_temp

    for step in range(max_steps):
        conflicts = count_conflicts(state)
        if conflicts == 0:
            return state, step
        row = random.randint(0, n - 1)
        new_col = random.randint(0, n - 1)
        old_col = state[row]
        state[row] = new_col
        new_conflicts = count_conflicts(state)
        delta = new_conflicts - conflicts
        if delta <= 0 or random.random() < math.exp(-delta / temp):
            pass  
        else:
            state[row] = old_col 
        temp *= cooling_rate
        if temp < 0.001:
            break
    return None, max_steps

if __name__ == "__main__":
    N = 10

    tracemalloc.start()
    start_time = time.time()

    solution, steps = simulated_annealing(N)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    if solution:
        print("The solution has been found.")
        print("Positions:", solution)
    else:
        print("No solution found.")
    print(f"Steps: {steps}")
    print(f"Lead time: {end_time - start_time:.4f} seconds")
    print(f"Memory usage: {peak / 1024:.2f} KB")
