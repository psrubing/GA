from Population import Population
import config


def main():
    pop = Population(config.pop_size)
    pop.make_population()
    pop.makedir()
    pop.write_input(config.patterns)
    pop.simulation_nominal()
    pop.simulation_void()
    pop.get_k_nominal()
    pop.get_k_void()

    lowest = pop.worst_chromosome()
    pop.calc_pop_fitness(lowest, pop.generation)
    pop.write_output(0, lowest)

    for generation in range(config.num_generations):

        new_pop = Population(config.pop_size)

        for i in range(int(config.pop_size / 2)):
            parent1 = pop.roulette(lowest, pop.generation)
            parent2 = pop.roulette(lowest, pop.generation)

            child1, child2 = pop.crossover(parent1, parent2)

            new_pop.chromosomes.append(child1)
            new_pop.chromosomes.append(child2)

        pop = new_pop
        pop.generation = generation + 1
        pop.mutation(config.mutation_prob)
        pop.makedir()
        pop.write_input(config.patterns)
        pop.simulation_nominal()
        pop.simulation_void()
        pop.get_k_nominal()
        pop.get_k_void()

        pop.calc_pop_fitness(lowest, pop.generation)

        pop.write_output(1, lowest)


if __name__ == '__main__':
    main()
