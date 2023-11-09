import random
import matplotlib.pyplot as plt
import math
GRID_SIZE = 5

fpga_grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def calculate_wirelength(placement):
    total_wirelength = 0
    for block_a in placement:
        for block_b in placement:
            if block_a != block_b:
                x1, y1 = block_a
                x2, y2 = block_b
                distance = abs(x2 - x1) + abs(y2 - y1)  # Manhattan distance
                total_wirelength += distance
    return total_wirelength

def simulated_annealing(initial_placement, temperature, cooling_rate, iterations):
    current_placement = initial_placement
    best_placement = initial_placement
    wirelengths = []

    for i in range(iterations):
        next_placement = current_placement.copy()
        block_to_move = random.choice(next_placement)
        next_x = (block_to_move[0] + random.choice([-1, 1])) % GRID_SIZE
        next_y = (block_to_move[1] + random.choice([-1, 1])) % GRID_SIZE
        next_placement.remove(block_to_move)
        next_placement.append((next_x, next_y))

        current_wirelength = calculate_wirelength(current_placement)
        next_wirelength = calculate_wirelength(next_placement)
        wirelengths.append(current_wirelength)

        if next_wirelength < current_wirelength:
            current_placement = next_placement
            if next_wirelength < calculate_wirelength(best_placement):
                best_placement = next_placement
        else:
            probability = math.exp(-(next_wirelength - current_wirelength) / temperature)
            if random.random() < probability:
                current_placement = next_placement

        temperature *= cooling_rate

    return best_placement, wirelengths

def plot_wirelength(iterations, wirelengths, cooling_rate):
    plt.plot(range(iterations), wirelengths, label=f"Cooling Rate: {cooling_rate}")
    plt.xlabel('Iterations')
    plt.ylabel('Wirelength')
    plt.title('Wirelength changes over iterations')
    plt.legend()
    plt.show()



# Different scenarios with varying parameters
cooling_rates = [0.95, 0.98, 0.99]
num_iterations = 5000
initial_temperature = 1000.0

for rate in cooling_rates:
    initial_placement = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(5)]
    best_placement, wirelengths = simulated_annealing(initial_placement, initial_temperature, rate, num_iterations)
    
    print(f"Best Placement with Cooling Rate {rate}: {best_placement}")
    print(f"Minimum Wirelength with Cooling Rate {rate}: {calculate_wirelength(best_placement)}")

    plot_wirelength(num_iterations, wirelengths, rate)
