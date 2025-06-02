import random
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

def hill_climbing(n, max_steps=1000):
    state = [random.randint(0, n - 1) for _ in range(n)]
    for step in range(max_steps):
        conflicts = count_conflicts(state)
        if conflicts == 0:
            return state, step
        best_state = state[:]
        best_conflicts = conflicts
        for row in range(n):
            original_col = state[row]
            for col in range(n):
                if col == original_col:
                    continue
                state[row] = col
                temp_conflicts = count_conflicts(state)
                if temp_conflicts < best_conflicts:
                    best_state = state[:]
                    best_conflicts = temp_conflicts
            state[row] = original_col
        if best_conflicts >= conflicts:
            break
        state = best_state
    return None, max_steps

if __name__ == "__main__":
    N = 10
    max_restarts = 100
    total_steps = 0
    found_solution = None

    tracemalloc.start()
    start_time = time.time()

    for attempt in range(max_restarts):
        solution, steps = hill_climbing(N)
        total_steps += steps
        if solution:
            found_solution = solution
            break

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    if found_solution:
        print(f"The solution was found  {attempt + 1}!")
        print("Positions:", found_solution)
    else:
        print(f"No solution found. {max_restarts}")
    print(f"Steps: {total_steps}")
    print(f"Lead time: {end_time - start_time:.4f} seconds")
    print(f"Memory usage: {peak / 1024:.2f} KB")
