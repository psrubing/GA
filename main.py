from Population import Population
import random


def main():
    num_generations = 50
    pop_size = 10
    mutation_prob = 0.001
    best_path = "/home/piotrs/GA/Core+Boron/Best_Chromosomes.txt"
    patterns = ["/home/piotrs/GA/Core+Boron/input_nominal.inp", "/home/piotrs/GA/Core+Boron/input_void.inp"]

    pop = Population(pop_size)
    pop.make_population()
    pop.makedir()
    pop.write_input(patterns)
    pop.simulation_nominal()
    pop.simulation_void()
    pop.get_k_nominal()
    pop.get_k_void()
    pop.calc_pop_fitness()

    best_input = open(best_path, "a+")
    best_input.write(
        "Generation\tPopulation Fitness\tBest Chromosome Fitness\t\tBest Chromosome\t\tkeff_nominal\t\tkeff_void\t\tSVR\n")
    best_input.write(
        str(pop.generation) + "\t\t" + str(pop.pop_fitness) + "\t" + str(pop.best_chromosome(0)) + "\t\t" + str(
            pop.best_chromosome(1))
        + "\t\t" + str(pop.best_chromosome(2)) + "\t\t\t" + str(pop.best_chromosome(3)) + "\t\t" + str(
            pop.best_chromosome(4)) + "\n")
    best_input.close()

    for generation in range(num_generations):

        new_pop = Population(pop_size)
        best_input = open(best_path, "a+")

        for i in range(int(pop_size / 2)):
            parent1 = pop.roulette()
            parent2 = pop.roulette()

            child1, child2 = pop.crossover(parent1, parent2)

            new_pop.chromosomes.append(child1)
            new_pop.chromosomes.append(child2)

        pop = new_pop
        pop.generation = generation + 1
        pop.mutation(mutation_prob)
        pop.makedir()
        pop.write_input(patterns)
        pop.simulation_nominal()
        pop.simulation_void()
        pop.get_k_nominal()
        pop.get_k_void()
        pop.calc_pop_fitness()

        print(f"Population nr. {pop.generation} fitness: ", pop.pop_fitness)
        best_input.write(
            str(pop.generation) + "\t\t" + str(pop.pop_fitness) + "\t" + str(pop.best_chromosome(0)) + "\t\t" + str(
                pop.best_chromosome(1))
            + "\t\t" + str(pop.best_chromosome(2)) + "\t\t\t" + str(pop.best_chromosome(3)) + "\t\t" + str(
                pop.best_chromosome(4)) + "\n")
        best_input.close()


if __name__ == '__main__':
    main()
