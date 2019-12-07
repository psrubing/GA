from Population import Population


def main():
    num_generations = 50
    pop_size = 50
    mutation_prob = 0.001

    pop = Population(pop_size)
    pop.make_population()
    pop.makedir()
    pop.simulation()
    pop.calc_pop_fitness()

    best_path = "/home/piotrs/GA/Core+Boron/Best_Chromosomes.txt"
    best_input = open(best_path, "a+")
    best_input.write("Generation\tPopulation Fitness\tBest Chromosome Fitness\t\tBest Chromosome\t\tkeff_nominal\t\tkeff_void\n")
    best_input.write(str(pop.generation) + "\t\t" + str(pop.pop_fitness) + "\t" + str(pop.best_chromosome(0)) + "\t\t" + str(pop.best_chromosome(1))
                     + "\t" + str(pop.best_chromosome(2)) + "\t\t" + str(pop.best_chromosome(3)) + "\n")
    best_input.close()

    for generation in range(num_generations):

        new_pop = Population(pop_size)
        best_input = open(best_path, "a+")

        for i in range(int(pop_size / 2)):
            parent1 = pop.roulette()
            parent2 = pop.roulette()

            # print("parent1: ", parent1)
            # print("parent2: ", parent2)

            child1, child2 = pop.crossover(parent1, parent2)

            # print("child1: ", child1)
            # print("child2: ", child2)

            new_pop.chromosomes.append(child1)
            new_pop.chromosomes.append(child2)

        pop = new_pop
        pop.generation = generation + 1
        pop.mutation(mutation_prob)
        pop.makedir()
        pop.simulation()
        pop.calc_pop_fitness()

        print("Best chromosome from population nr. {} : {}\n".format(pop.generation, pop.best_chromosome()))
        print(f"Population nr. {pop.generation} fitness: ", pop.pop_fitness)
        best_input.write(str(pop.generation) + "\t\t" + str(pop.pop_fitness) + "\t" + str(pop.best_chromosome(0)) + "\t\t" + str(pop.best_chromosome(1))
            + "\t" + str(pop.best_chromosome(2)) + "\t\t" + str(pop.best_chromosome(3)) + "\n")
        best_input.close()


if __name__ == '__main__':
    main()
