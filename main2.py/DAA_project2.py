import random
import math
import time
import statistics
import csv


def orientation(p, q, r):
    return (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])


def convex_hull_optimized(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    def build_hull(points):
        hull = []
        for p in points:

            while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) <= 0:
                hull.pop()
            hull.append(p)
        return hull

    lower = build_hull(points)
    upper = build_hull(reversed(points))
    return lower + upper[1:-1]


def theoretical_time(n):
    return 10 * n * math.log2(n) + 50 * n + 1000


def generate_points(n, seed=None):
    if seed is not None:
        random.seed(seed)
    return [(random.randint(0, 1000000), random.randint(0, 1000000)) for _ in range(n)]


def run_experiment(n, num_trials=5):
    experimental_times = []
    for _ in range(num_trials):
        points = generate_points(n)
        start_time = time.perf_counter()
        hull = convex_hull_optimized(points)
        end_time = time.perf_counter()
        experimental_times.append(end_time - start_time)
    return statistics.mean(experimental_times), len(hull)


n_values = [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
            2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000,
            3100, 3200, 3300, 3400, 3500, 3600, 3700, 3800]

results = []

for n in n_values:
    exp_time, hull_size = run_experiment(n)
    theo_time = theoretical_time(n)
    results.append((n, hull_size, exp_time, theo_time))

print(f"{'n Values':<10} {'Points in Hull':<15} {'Exp Time (s)':<15} {'Theo Time':<15}")
print("=" * 55)
for n, hull_size, exp_time, theo_time in results:
    print(f"{n:<10} {hull_size:<15} {exp_time:<15.6f} {theo_time:<15.2f}")

with open('convex_hull_analysis.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['n', 'Points in Hull', 'Experimental Time (s)', 'Theoretical Time'])
    writer.writerows(results)

print("Analysis complete. Results saved to 'convex_hull_analysis.csv'.")
