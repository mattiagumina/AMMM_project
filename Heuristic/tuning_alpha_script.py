import matplotlib.pyplot as plt
from solvers.solver_GRASP import Solver_GRASP
from datParser import DATParser

alphas = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

input_data = DATParser.parse("instance40_0.dat")
y40_optimal = 0.525238095238095
y40_obtained = [0] * 11

index = 0
for alpha in alphas:
    solver = Solver_GRASP(input_data, 10000, alpha)

    obj = 0
    i = 0
    while i < 50:
        solver.current_committee = []
        try:
            solver._greedy_randomized_construction()
            obj += solver._calculate_avg_compatibility(solver.current_committee)
            i += 1
        except ValueError:
            continue # Skip invalid constructions

    y40_obtained[index] = obj / 50
    index += 1

input_data = DATParser.parse("instance50_0.dat")
y50_optimal = 0.548874458874459
y50_obtained = [0] * 11

index = 0
for alpha in alphas:
    solver = Solver_GRASP(input_data, 10000, alpha)

    obj = 0
    i = 0
    while i < 50:
        solver.current_committee = []
        try:
            solver._greedy_randomized_construction()
            obj += solver._calculate_avg_compatibility(solver.current_committee)
            i += 1
        except ValueError:
            continue # Skip invalid constructions

    y50_obtained[index] = obj / 50
    index += 1

input_data = DATParser.parse("instance60_0.dat")
y60_optimal = 0.511390374331551
y60_obtained = [0] * 11

index = 0
for alpha in alphas:
    solver = Solver_GRASP(input_data, 10000, alpha)

    obj = 0
    i = 0
    while i < 50:
        solver.current_committee = []
        try:
            solver._greedy_randomized_construction()
            obj += solver._calculate_avg_compatibility(solver.current_committee)
            i += 1
        except ValueError:
            continue # Skip invalid constructions

    y60_obtained[index] = obj / 50
    index += 1

gap40 = [100 - y40_obtained[i] / y40_optimal * 100 for i in range(11)]
gap50 = [100 - y50_obtained[i] / y50_optimal * 100 for i in range(11)]
gap60 = [100 - y60_obtained[i] / y60_optimal * 100 for i in range(11)]

plt.plot(alphas, gap40, marker='o', label='N = 40')
plt.plot(alphas, gap50, marker='o', label='N = 50')
plt.plot(alphas, gap60, marker='o', label='N = 60')
plt.xlabel('Alpha')
plt.ylabel('Relative gap (%)')
plt.title('Tuning Alpha Parameter')
plt.legend()
plt.grid(True)
plt.show()
