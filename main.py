from Population import Population


def main():
    num_generations = 50
    pop_size = 50
    mutation_prob = 0.01
    best_path = "/home/piotrs/GA/Best_Chromosomes.txt"

    pop = Population(pop_size)
    pop.make_population()
    print("Zero's pop fitness: ", pop.calc_pop_fitness())

    best_input = open(best_path, "a+")
    best_input.write("Generation\tBest Fitness\t\tChromosome:\n")

    for generation in range(num_generations):

        new_pop = Population(pop_size)

        for i in range(int(pop_size / 2)):
            parent1 = pop.roulette()
            parent2 = pop.roulette()

            print("parent1: ", parent1)
            print("parent2: ", parent2)

            child1, child2 = pop.crossover(parent1, parent2)

            print("child1: ", child1)
            print("child2: ", child2)

            new_pop.chromosomes.append(child1)
            new_pop.chromosomes.append(child2)

        pop = new_pop
        pop.generation = generation + 1
        pop.mutation(mutation_prob)
        pop.makedir()
        pop.simulation()

        print("Best chromosome from population nr. {} : {}\n".format(pop.generation, pop.best_chromosome()))
        print(f"New pop nr. {pop.generation} fitness: ", pop.calc_pop_fitness())
        best_input.write(str(pop.generation)+"\t\t"+str(pop.best_chromosome(1))+"\t"+str(pop.best_chromosome(0))+"\n")

    best_input.close()


if __name__ == '__main__':
    main()
