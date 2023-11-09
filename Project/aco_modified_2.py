import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class FPGA:
    def __init__(self, width, height, num_tracks):
        self.width = width
        self.height = height
        self.num_tracks = num_tracks
        self.grid = np.zeros((height, width, num_tracks), dtype=float)
        self.obstacles = set()

    def place_obstacles(self, num_obstacles):
        for _ in range(num_obstacles):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.obstacles.add((x, y))

class Ant:
    def __init__(self, fpga):
        self.fpga = fpga
        self.placement = [(random.randint(0, fpga.width - 1), random.randint(0, fpga.height - 1))]

    def move(self):
        x, y = self.placement[-1]
        possible_moves = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
        valid_moves = [move for move in possible_moves if 0 <= move[0] < self.fpga.width and 0 <= move[1] < self.fpga.height and move not in self.fpga.obstacles]
        if valid_moves:
            new_x, new_y = random.choice(valid_moves)
            self.placement.append((new_x, new_y))

def update_pheromones_logic1(ants):
    evaporation_rate = 0.1
    deposit_rate = 0.5

    for ant in ants:
        for x, y in ant.placement:
            ant.fpga.grid[y, x, :] += deposit_rate

    ants[0].fpga.grid = ants[0].fpga.grid * (1 - evaporation_rate)

def update_pheromones_logic2(ants):
    evaporation_rate = 0.1
    deposit_rate = 0.1

    for ant in ants:
        for x, y in ant.placement:
            ant.fpga.grid[y, x, :] += deposit_rate

    ants[0].fpga.grid = ants[0].fpga.grid * (1 - evaporation_rate)

def evaluate_solution(placement, fpga):
    return np.sum(fpga.grid)

def visualize_fpga_routing(fpga, placement, title):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(0, fpga.width)
    ax.set_ylim(0, fpga.height)

    for x, y in fpga.obstacles:
        ax.add_patch(Rectangle((x, y), 1, 1, color='red', alpha=0.7))

    for x, y in placement:
        ax.add_patch(Rectangle((x, y), 1, 1, color='blue', alpha=0.7))

    plt.title(title)
    plt.show()

def plot_wirelength(iterations, wirelengths, logic_name):
    plt.plot(iterations, wirelengths, label=logic_name)
    plt.xlabel('Iterations')
    plt.ylabel('Wirelength')
    plt.title('Wirelength vs. Number of Iterations')
    plt.legend()
    plt.grid(True)

def main_more_ants_less_iterations():
    fpga = FPGA(width=10, height=10, num_tracks=4)
    fpga.place_obstacles(num_obstacles=5)

    num_ants = 20  # Increase the number of ants
    ants = [Ant(fpga) for _ in range(num_ants)]

    num_iterations = 50  # Decrease the number of iterations
    iterations = list(range(1, num_iterations + 1))
    wirelengths_logic1 = []
    wirelengths_logic2 = []

    for iteration in range(num_iterations):
        for ant in ants:
            ant.move()
        update_pheromones_logic1(ants)

        best_solution_logic1 = None

        for ant in ants:
            solution = (ant.placement, ant.fpga)

            if best_solution_logic1 is None or evaluate_solution(*solution) < evaluate_solution(*best_solution_logic1):
                best_solution_logic1 = solution

        wirelength_logic1 = evaluate_solution(best_solution_logic1[0], fpga)
        wirelengths_logic1.append(wirelength_logic1)

        # Logic 2
        for ant in ants:
            ant.move()
        update_pheromones_logic2(ants)

        best_solution_logic2 = None

        for ant in ants:
            solution = (ant.placement, ant.fpga)

            if best_solution_logic2 is None or evaluate_solution(*solution) < evaluate_solution(*best_solution_logic2):
                best_solution_logic2 = solution

        wirelength_logic2 = evaluate_solution(best_solution_logic2[0], fpga)
        wirelengths_logic2.append(wirelength_logic2)

    plt.figure(figsize=(10, 6))
    plot_wirelength(iterations, wirelengths_logic1, 'Logic 1 (More Ants, Less Iterations)')
    plot_wirelength(iterations, wirelengths_logic2, 'Logic 2 (More Ants, Less Iterations)')

    print("Final Wirelength for Logic 1 (More Ants, Less Iterations):", wirelength_logic1)
    print("Final Wirelength for Logic 2 (More Ants, Less Iterations):", wirelength_logic2)

    if wirelength_logic1 < wirelength_logic2:
        print("Logic 1 (More Ants, Less Iterations) is better.")
    elif wirelength_logic1 > wirelength_logic2:
        print("Logic 2 (More Ants, Less Iterations) is better.")
    else:
        print("Both logics have the same final wirelength (More Ants, Less Iterations).")

    visualize_fpga_routing(fpga, best_solution_logic1[0], 'Logic 1 Placement and Routing (More Ants, Less Iterations)')
    visualize_fpga_routing(fpga, best_solution_logic2[0], 'Logic 2 Placement and Routing (More Ants, Less Iterations)')

    plt.show()

def main_less_ants_more_iterations():
    fpga = FPGA(width=10, height=10, num_tracks=4)
    fpga.place_obstacles(num_obstacles=5)

    num_ants = 5  # Reduce the number of ants
    ants = [Ant(fpga) for _ in range(num_ants)]

    num_iterations = 200  # Increase the number of iterations
    iterations = list(range(1, num_iterations + 1))
    wirelengths_logic1 = []
    wirelengths_logic2 = []

    for iteration in range(num_iterations):
        for ant in ants:
            ant.move()
        update_pheromones_logic1(ants)

        best_solution_logic1 = None

        for ant in ants:
            solution = (ant.placement, ant.fpga)

            if best_solution_logic1 is None or evaluate_solution(*solution) < evaluate_solution(*best_solution_logic1):
                best_solution_logic1 = solution

        wirelength_logic1 = evaluate_solution(best_solution_logic1[0], fpga)
        wirelengths_logic1.append(wirelength_logic1)

        # Logic 2
        for ant in ants:
            ant.move()
        update_pheromones_logic2(ants)

        best_solution_logic2 = None

        for ant in ants:
            solution = (ant.placement, ant.fpga)

            if best_solution_logic2 is None or evaluate_solution(*solution) < evaluate_solution(*best_solution_logic2):
                best_solution_logic2 = solution

        wirelength_logic2 = evaluate_solution(best_solution_logic2[0], fpga)
        wirelengths_logic2.append(wirelength_logic2)

    plt.figure(figsize=(10, 6))
    plot_wirelength(iterations, wirelengths_logic1, 'Logic 1 (Less Ants, More Iterations)')
    plot_wirelength(iterations, wirelengths_logic2, 'Logic 2 (Less Ants, More Iterations)')

    print("Final Wirelength for Logic 1 (Less Ants, More Iterations):", wirelength_logic1)
    print("Final Wirelength for Logic 2 (Less Ants, More Iterations):", wirelength_logic2)

    if wirelength_logic1 < wirelength_logic2:
        print("Logic 1 (Less Ants, More Iterations) is better.")
    elif wirelength_logic1 > wirelength_logic2:
        print("Logic 2 (Less Ants, More Iterations) is better.")
    else:
        print("Both logics have the same final wirelength (Less Ants, More Iterations).")

    visualize_fpga_routing(fpga, best_solution_logic1[0], 'Logic 1 Placement and Routing (Less Ants, More Iterations)')
    visualize_fpga_routing(fpga, best_solution_logic2[0], 'Logic 2 Placement and Routing (Less Ants, More Iterations)')

    plt.show()

def main():
    print("Case 1: More Ants with Fewer Iterations")
    main_more_ants_less_iterations()
    
    print("\nCase 2: Fewer Ants with More Iterations")
    main_less_ants_more_iterations()

if __name__ == "__main__":
    main()
