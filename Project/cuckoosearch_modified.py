import numpy as np
import random
import matplotlib.pyplot as plt

class CuckooSearch:
    def __init__(self, n_nodes, n_cells, alpha, beta, p):
        self.n_nodes = n_nodes
        self.n_cells = n_cells
        self.alpha = alpha
        self.beta = beta
        self.p = p

        # Initialize the cuckoo nests
        self.nests = np.zeros((n_cells, n_nodes))
        for i in range(n_cells):
            for j in range(n_nodes):
                self.nests[i][j] = random.randint(0, n_nodes - 1)

    def update(self, nest):
        # Modified update function for Case 1
        if random.random() < self.alpha:
            # Swap two random nodes in the nest
            node1, node2 = random.randint(0, self.n_nodes - 1), random.randint(0, self.n_nodes - 1)
            nest[node1], nest[node2] = nest[node2], nest[node1]

        # Modified update function for Case 2
        elif random.random() < self.beta:
            # Move a random node to a randomly selected empty cell
            node = random.randint(0, self.n_nodes - 1)
            empty_cell = random.randint(0, self.n_cells - 1)
            if self.nests[empty_cell][node] == 0:
                nest[node] = empty_cell

    def run(self, iterations):
        # Keep iterating until the maximum number of iterations is reached
        for i in range(iterations):
            # For each cuckoo nest, update it according to the update function
            for nest in self.nests:
                self.update(nest)

        # Return the best nest found
        return self.nests[np.argmin(self.get_wirelength())]

    def get_wirelength(self):
        # Calculate the wirelength of each nest
        wirelengths = np.zeros(len(self.nests))
        for i in range(len(self.nests)):
            # Calculate the Manhattan distance between each node and its assigned cell
            node_to_cell_distances = np.zeros(self.n_nodes)
            for j in range(self.n_nodes):
                node_to_cell_distances[j] = np.abs(self.nests[i][j] - j)

            # Calculate the total wirelength of the nest
            wirelengths[i] = np.sum(node_to_cell_distances)

        return wirelengths

# Test cases

# Case 1: Update function with swapping of two random nodes
test_case_1 = CuckooSearch(n_nodes=10, n_cells=10, alpha=0.5, beta=0.5, p=0.5)
best_nest_1 = test_case_1.run(iterations=100)

# Case 2: Update function with moving a random node to a randomly selected empty cell
test_case_2 = CuckooSearch(n_nodes=10, n_cells=10, alpha=0.5, beta=0.5, p=0.5)
best_nest_2 = test_case_2.run(iterations=100)

# Graphical representation of the wirelength vs iterations

plt.figure()
plt.plot(test_case_1.get_wirelength(), label="Case 1")
plt.plot(test_case_2.get_wirelength(), label="Case 2")
plt.xlabel("Iterations")
plt.ylabel("Wirelength")
plt.legend()
plt.show()

# Display the best nest and wirelength details for each case

def display_best_nest_and_wirelength(test_case, best_nest, wirelength):
  print("Case:", test_case)
  print("Best nest:", best_nest)
  print("Wirelength:", wirelength)

display_best_nest_and_wirelength("Case 1", best_nest_1, test_case_1.get_wirelength()[np.argmin(test_case_1.get_wirelength())])
display_best_nest_and_wirelength("Case 2", best_nest_2, test_case_2.get_wirelength()[np.argmin(test_case_2.get_wirelength())])
