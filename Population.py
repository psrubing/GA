import random
import os
from Chromosome import Chromosome

class Population:

    def __init__(self, pop_size):
        self.chromosomes = []
        self.size = pop_size
        self.generation = 0
        self.pop_fitness = 0
        self.dir_path = "/home/piotrs/GA/Generation_"


    def make_population(self):

        for i in range(self.size):
            self.chromosomes.append(Chromosome())

    def calc_pop_fitness(self):

        for chromosome in self.chromosomes:
            self.pop_fitness += chromosome.get_fitness()
        return self.pop_fitness

    def roulette(self):

        pick = random.uniform(0, self.pop_fitness)
        sum_level = 0

        for chromosome in self.chromosomes:
            sum_level += chromosome.get_fitness()
            if sum_level > pick:
                return chromosome

    def crossover(self, parent1, parent2):

        crossover_point = random.randint(0, Chromosome.chromosome_length)

        child1 = Chromosome((parent1.chromosome_list[0:crossover_point] + parent2.chromosome_list[crossover_point:]))
        child2 = Chromosome((parent2.chromosome_list[0:crossover_point] + parent1.chromosome_list[crossover_point:]))

        return child1, child2

    def mutation(self, probability=0.0):

        new_chromosomes = []
        for chromosome in self.chromosomes:
            new_chromosome = []
            for gene in chromosome.chromosome_list:
                random_value = random.uniform(0, 1)
                if random_value < probability:
                    if int(gene) == 1:
                        new_chromosome.append(0)
                    elif int(gene) == 0:
                        new_chromosome.append(1)
                else:
                    new_chromosome.append(gene)

            new_chromosomes.append(Chromosome(new_chromosome))
        self.chromosomes = new_chromosomes

    def best_chromosome(self,fit_or_chrom = 0):
        best = 0.0
        for chromosome in self.chromosomes:
            if best < chromosome.get_fitness():
                best = chromosome.get_fitness()
                best_chromosome = chromosome.chromosome_dec
        if fit_or_chrom == 0:
            return best_chromosome
        elif fit_or_chrom == 1:
            return best

    def makedir(self):
        os.mkdir(self.dir_path + str(self.generation))

    def simulation(self):
        counter = 1
        for chromosome in self.chromosomes:
            pattern = open("/home/piotrs/GA/input.inp", "r")
            chromosome_path = self.dir_path +str(self.generation)+"/" + str(counter) + "_" + str(chromosome.chromosome_dec)+".inp"
            chromosome_input = open(chromosome_path, "w")
            for line in pattern:
                if "{}" in line:
                    line = line.replace("{}", str(chromosome.get_uranium_radius()))
                if "[]" in line:
                    line = line.replace("[]", str(chromosome.get_water_radius()))
                chromosome_input.write(line)

            pattern.close()
            chromosome_input.close()

            bash_path = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(chromosome.chromosome_dec) + ".sh"
            bash_input = open(bash_path, "w")
            bash_cmd = "#!/bin/bash\n/home/piotrs/GA/sss2 -omp 4 "
            bash_input.write(bash_cmd + self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(chromosome.chromosome_dec) + ".inp")
            bash_input.close()

            print("\nSymulacja dla chromosomu: {} z pokolenia {}".format(chromosome,self.generation))
            os.system("bash "+bash_path)

            chromosome_output = open(chromosome_path + "_res.m", "r")
            for line in chromosome_output:
                if "ABS_KEFF" in line:
                    chromosome.keff = float(line[47:58])

            counter += 1
