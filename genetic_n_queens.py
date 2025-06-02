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

def crossover(parent1, parent2):
    n = len(parent1)
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(state, mutation_rate=0.1):
    n = len(state)
    for i in range(n):
        if random.random() < mutation_rate:
            state[i] = random.randint(0, n - 1)
    return state

def genetic_algorithm(n, population_size=100, generations=1000):
    population = [[random.randint(0, n - 1) for _ in range(n)] for _ in range(population_size)]

    for gen in range(generations):
        population.sort(key=count_conflicts)
        if count_conflicts(population[0]) == 0:
            return population[0], gen

        new_population = population[:10]  # элита
        while len(new_population) < population_size:
            parents = random.sample(population[:50], 2)
            child = crossover(parents[0], parents[1])
            child = mutate(child)
            new_population.append(child)
        population = new_population

    return None, generations


if __name__ == "__main__":
    N = 10

    tracemalloc.start()
    start_time = time.time()

    solution, generations = genetic_algorithm(N)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    if solution:
        print(f"The solution is found {generations}!")
        print("Positions:", solution)
    else:
        print("No solution found.")
    print(f"Lead time:{end_time - start_time:.4f} seconds")
    print(f"Memory usage: {peak / 1024:.2f} KB")

