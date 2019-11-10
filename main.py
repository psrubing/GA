from Population import Population

def main():

    num_generations = 100
    pop_size = 50

    pop = Population(pop_size)
    pop.make_population()
    print("First pop fitness: ", pop.calc_pop_fitness())

    for generation in range(num_generations):

        new_pop = Population(pop_size)

        for i in range(int(pop_size/2)):

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
        pop.mutation(0.01)
        pop.generation += 1

        print("Best chromosome from pop: ",pop.best_chromosome())
        print(f"New pop nr. {generation} fitness: ", pop.calc_pop_fitness())


if __name__ == '__main__':
    main()