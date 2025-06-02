import time
import tracemalloc

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

if __name__ == "__main__":
    N = 10

    tracemalloc.start()
    start_time = time.time()

    solutions = solve_dfs(N)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"N = {N}")
    print(f"Solutions found: {len(solutions)}")
    print(f"Lead time: {end_time - start_time:.4f} seconds")
    print(f"Memory usage: {peak / 1024:.2f} KB")


