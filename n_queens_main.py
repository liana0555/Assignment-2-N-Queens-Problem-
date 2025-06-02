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

def is_valid(state):
    return count_conflicts(state) == 0

def is_safe(position, row, col):
    for r in range(row):
        c = position[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def solve_dfs(n):
    solutions = []
    def dfs(row, position):
        if row == n:
            solutions.append(position[:])
            return
        for col in range(n):
            if is_safe(position, row, col):
                position[row] = col
                dfs(row + 1, position)
    position = [-1] * n
    dfs(0, position)
    return solutions

def hill_climbing(n, max_steps=1000):
    state = [random.randint(0, n - 1) for _ in range(n)]
    for step in range(max_steps):
        conflicts = count_conflicts(state)
        if conflicts == 0:
            return state, step, state
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
    return None, max_steps, state

def simulated_annealing(n, max_steps=500000, start_temp=100, cooling_rate=0.995, restarts=10):
    for attempt in range(restarts):
        state = [random.randint(0, n - 1) for _ in range(n)]
        initial = state[:]
        temp = start_temp
        for step in range(max_steps):
            conflicts = count_conflicts(state)
            if conflicts == 0:
                return state, step, initial
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
    return None, max_steps * restarts, initial

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 2)
    return p1[:point] + p2[point:]

def mutate(state, rate=0.1):
    for i in range(len(state)):
        if random.random() < rate:
            state[i] = random.randint(0, len(state) - 1)
    return state

def genetic_algorithm(n, pop_size=100, generations=1000):
    population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(pop_size)]
    initial = population[0][:]
    for gen in range(generations):
        population.sort(key=count_conflicts)
        if count_conflicts(population[0]) == 0:
            return population[0], gen, initial
        new_pop = population[:10]
        while len(new_pop) < pop_size:
            parents = random.sample(population[:50], 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child)
            new_pop.append(child)
        population = new_pop
    return None, generations, initial


def print_board(state):
    n = len(state)
    for row in range(n):
        board = ['.'] * n
        if 0 <= state[row] < n:
            board[state[row]] = '♛'
        print(" ".join(board))

if __name__ == "__main__":
    sizes = [10, 30, 50, 100]
    print("Choose the board size:")
    for i, n_val in enumerate(sizes):
        print(f"{i + 1} - N = {n_val}")
    choice = input("Your number of choice:").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(sizes)):
        print("Wrong choice")
        exit()

    n = sizes[int(choice) - 1]

    algorithms = [
        ("DFS", solve_dfs if n <= 15 else None),
        ("Hill Climbing", hill_climbing),
        ("Simulated Annealing", simulated_annealing),
        ("Genetic Algorithm", genetic_algorithm)
    ]

    for name, algorithm in algorithms:
        if algorithm is None:
            print(f"\n {name} Skipped, too slow for N = {n})")
            continue

        print(f"\n=== {name} ===")
        tracemalloc.start()
        start_time = time.time()

        if name == "DFS":
            solutions = algorithm(n)
            result = solutions[0] if solutions else None
            steps = "All solutions"
            initial = "It doesn't matter"
        else:
            result, steps, initial = algorithm(n)

        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("\nInitial state:")
        if isinstance(initial, list) and n <= 50:
            print_board(initial)
        else:
            print("Hidden for N > 50")

        if result and is_valid(result):
            print("\n The solution has been found")
            if n <= 50:
                print_board(result)
            else:
                print("Hidden for N > 50")
        elif result:
            print("\n Incorrect")
            if n <= 50:
                print_board(result)
            else:
                print("Hidden for N > 50")
        else:
            print("\nNo solution found")

        print(f"\nSteps: {steps}")
        print(f"Lead time: {end_time - start_time:.4f} seconds")
        print(f"Memory usage:{peak / 1024:.2f} KB")
