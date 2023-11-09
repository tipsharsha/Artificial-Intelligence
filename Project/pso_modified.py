import random
import numpy as np
import tkinter as tk
import tkinter.messagebox as messagebox
import time
def random_color():
    number_of_colors = 8
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
            
    return color

class Particle:
    def __init__(self, num_nodes, num_edges):
        self.position = self.generate_random_position(num_nodes)
        self.velocity = self.generate_random_position(num_nodes)
        self.best_position = self.position
        self.fitness = self.calculate_fitness()

    def generate_random_position(self, num_nodes):
        return [np.array([random.randint(0, 50), random.randint(0, 50)]) for _ in range(num_nodes)]

    def calculate_fitness(self):
        # Calculate the fitness of a particle
        placement_fitness = sum([abs(x[0] - x[1]) for x in self.position])
        return 100 - placement_fitness  # Inverse fitness (higher value is better)

class PSO:
    def __init__(self, num_particles, num_nodes, num_edges, max_iterations,canvas):
        self.num_particles = num_particles
        self.num_nodes = num_nodes
        self.num_edges = num_edges
        self.max_iterations = max_iterations
        self.global_best_position = None
        self.global_best_fitness = -float('inf')
        self.particles = [Particle(num_nodes, num_edges) for _ in range(num_particles)]
        
    def update_global_best(self,canvas):
        for i in range(len(self.particles)):
            particle = self.particles[i]
            if particle.fitness > self.global_best_fitness:
                self.global_best_fitness = particle.fitness
                self.global_best_position = particle.position

    def update_particle(self, particle,canvas):
        inertia_weight = 0.7
        cognitive_weight = 1.5
        social_weight = 1.5
        r1 = random.random()
        r2 = random.random()
        for v in particle.velocity:
            inert_v = [inertia_weight*x for x in v]
            new_velocity = [inert_v + cognitive_weight * r1 * (p - x) + social_weight * r2 * np.subtract(self.global_best_position[i], x)
                            for i, (x, p) in enumerate(zip(particle.position,  particle.best_position))]
        particle.velocity = new_velocity
        particle.position = [(x + v, y + w) for (x, y), (v, w) in zip(particle.position, particle.velocity)]
        particle.fitness = particle.calculate_fitness()

        if particle.fitness > particle.calculate_fitness():
            particle.best_position = particle.position

    def run_pso(self,canvas):
        for iteration in range(self.max_iterations):
            canvas.create_text(100, 100, text=f"Iteration: {iteration+1}/{self.max_iterations}",fill = 'red',font = ("Helvetica", 16))
            canvas.create_text(100, 120, text="Color: particle", fill="red",font = ("Helvetica", 16))
            canvas.create_text(170,140,text = "Number : Block number of particle",font = ("Helvetica", 16),fill = "red")
            self.update_global_best(canvas)
            for j in range(num_particles):
                    col = [random_color() for i in range(num_nodes)]
                    for i in range(num_nodes):
                        draw_block(canvas, self.particles[j].position[i][0], self.particles[j].position[i][1], i,col[i] )
            canvas.update()
            canvas.delete("all")
            # time.sleep(1)
            for particle in self.particles:
                self.update_particle(particle,canvas)
def draw_block(canvas, x,y,numn,fill='blue', outline='black'):
     # Adjust the scale for visualization
    # if(x<0):
    #       print("x is negative")
    canvas.create_rectangle(5*x+700, 4*y+300, 5*x + 730, 4*y + 330, fill=fill, outline=outline, tags=f'block{numn}')
    canvas.create_text(5*x+715, 4*y+315, text=f"{numn+1}")
if __name__ == '__main__':
    num_particles = 5
    num_nodes = 3
    num_edges = 20
    max_iterations = 10
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1920, height=1080, bg='black')
    canvas.pack()
    label = tk.Label(root, text="Particle swarm optimisation for FPGA", font=("Helvetica", 16), fg="blue", bg="black")
    label.place(x=570, y=10)
    pso = PSO(num_particles, num_nodes, num_edges, max_iterations,canvas)
    pso.run_pso(canvas)

    best_solution = pso.global_best_position
    best_fitness = pso.global_best_fitness

    print("Best Solution Fitness:", best_fitness)
    print("Best Solution Placement:")
    str = ""
    for i, (x, y) in enumerate(best_solution):
        str +=(f"Node {i+1}: ({x}, {y})\n")
    str = f"Best Solution Fitness: {best_fitness}\n"+"Best Solution Placement:\n"+str
    messagebox.showinfo("Best Solution", str)
    root.mainloop()
