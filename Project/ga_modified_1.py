import random
import statistics
from tkinter import *
import time
import tkinter.messagebox as messagebox

root = Tk()
root.config(padx=10,pady=10,bg = "black")
root.title("Genetic Algorithm")
canvas = Canvas(root, width=800, height=800, bg='black')

canvas.grid(row = 1,column = 0,columnspan =2)
FGCOLOR = "white"
lbel = Label(text = "Genetic Algorithm",fg = FGCOLOR,bg = "black",font = ("Helvetica", 16))
lbel.grid(row = 0,column = 0,columnspan = 2)
FONT = ("Helvetica", 16)

def random_color():
    number_of_colors = 8
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    return color


# Define your chromosome representation
class Chromosome:
    def __init__(self, placement, routing_info):
        self.placement = placement
        self.routing_info = routing_info
        self.fitness = 0

def initialize_population(population_size, num_nodes, num_edges):
    population = [Chromosome(generate_initial_placement(num_nodes), generate_initial_routing(num_edges)) for _ in range(population_size)]
    return population

def evaluate_fitness(chromosome):
    # Calculate the fitness of a chromosome
    chromosome.fitness = calculate_fitness(chromosome)

def select_parents_tournament(population, num_parents, tournament_size):
    parents = []
    for _ in range(num_parents):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda x: x.fitness)
        parents.append(winner)
    return parents

def select_parents_ranking(population, num_parents):
    ranked_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    ranked_fitness_values = [chromosome.fitness for chromosome in ranked_population]
    weights = [i for i in range(1, len(ranked_population) + 1)]
    parents = random.choices(ranked_population, weights=weights, k=num_parents)
    return parents

def select_parents_roulette_wheel(population, num_parents):
    total_fitness = sum(chromosome.fitness for chromosome in population)
    probabilities = [chromosome.fitness / total_fitness for chromosome in population]
    parents = random.choices(population, probabilities, k=num_parents)
    return parents

def crossover(parent1, parent2):
    crossover_point = len(parent1.placement) // 2
    child_placement = parent1.placement[:crossover_point] + parent2.placement[crossover_point:]
    child_routing_info = {**parent1.routing_info, **parent2.routing_info}
    child = Chromosome(child_placement, child_routing_info)
    return child

def mutate(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        mutate_placement(chromosome)
        mutate_routing_info(chromosome)

def replace_population(old_population, children):
    old_population.sort(key=lambda x: x.fitness)
    for i in range(len(children)):
        old_population[i] = children[i]
    return old_population

def generate_initial_placement(num_nodes):
    placement = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_nodes)]
    return placement

def generate_initial_routing(num_edges):
    routing_info = {edge: random.randint(1, 10) for edge in range(num_edges)}
    return routing_info

def calculate_fitness(chromosome):
    # Calculate the fitness of a chromosome
    # Alternative: Fitness as a function of placement and routing_info
    placement_fitness = sum([abs(x[0] - x[1]) for x in chromosome.placement])
    routing_fitness = max(chromosome.routing_info.values())
    total_fitness = placement_fitness + routing_fitness
    return 100 - total_fitness  # Inverse fitness (higher value is better)

def mutate_placement(chromosome):
    # Implement mutation of the placement
    # Alternative: Randomly swap two placement coordinates
    index1 = random.randint(0, len(chromosome.placement) - 1)
    index2 = random.randint(0, len(chromosome.placement) - 1)
    chromosome.placement[index1], chromosome.placement[index2] = chromosome.placement[index2], chromosome.placement[index1]

def mutate_routing_info(chromosome):
    # Implement mutation of routing information
    # Alternative: Randomly change one routing value
    edge_to_mutate = random.choice(list(chromosome.routing_info.keys()))
    chromosome.routing_info[edge_to_mutate] = random.randint(1, 10)

def run_genetic_algorithm(population_size, max_generations, mutation_rate, num_parents, num_children, num_nodes, num_edges, parent_selection_method):
    population = initialize_population(population_size, num_nodes, num_edges)
    for generation in range(max_generations):
        canvas.create_text(100, 700, text=f"Selection: {parent_selection_method} Color:Same Chromosome Number:Block Number of Chromosome", fill="white", font=("Helvetica", 13))
        for chromosome in population:
            evaluate_fitness(chromosome)

        if parent_selection_method == 'tournament':
            parents = select_parents_tournament(population, num_parents, tournament_size=5)
        elif parent_selection_method == 'ranking':
            parents = select_parents_ranking(population, num_parents)
        elif parent_selection_method == 'roulette_wheel':
            parents = select_parents_roulette_wheel(population, num_parents)

        children = []
        for _ in range(num_children):
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            children.append(child)
        for chromosome in population:
            display_chrome(chromosome)
        # time.sleep(1)
        root.update()
        canvas.delete("all")
        population = replace_population(population, children)
    best_solution = max(population, key=lambda x: x.fitness)
    return best_solution
def display_chrome(chrome):
    count = 1
    for place in chrome.placement:
        canvas.create_rectangle(6*place[0],6*place[1],6*place[0]+40,6*place[1]+40,fill=random_color())
        canvas.create_text(6*place[0]+20,6*place[1]+20,text = f"{count}",fill = "white",font = ("Helvetica", 16))
        count = count + 1

def compare_genetic_algorithms():
    parameter_configurations = [
        (10, 10, 0.01, 5, 5, 6, 20, 'tournament'),  # Configuration 1
        (10, 10, 0.01, 5, 5, 6, 20, 'ranking'),  # Configuration 2
        (10, 10, 0.01, 5, 5, 6, 20, 'roulette_wheel'),  # Configuration 3
        # Add more configurations here

    ]

    results = []

    for config in parameter_configurations:
        population_size, max_generations, mutation_rate, num_parents, num_children, num_nodes, num_edges, parent_selection_method = config
        best_solution = run_genetic_algorithm(population_size, max_generations, mutation_rate, num_parents, num_children, num_nodes, num_edges, parent_selection_method)
        results.append((config, best_solution))

    return results

analysis_results = compare_genetic_algorithms()

for config, best_solution in analysis_results:
    str = ""
    str +=f"Configuration: Population Size = {config[0]}, Generations = {config[1]}, Mutation Rate = {config[2]}, \nNum Parents = {config[3]}, Num Children = {config[4]}, Num Nodes = {config[5]}, Num Edges = {config[6]}, Parent Selection Method = {config[7]}"
    str += f"Best Solution Fitness: {best_solution.fitness}"
    messagebox.showinfo("Analysis",str)
root.mainloop()
