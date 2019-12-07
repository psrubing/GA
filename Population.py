import random
import os
from Chromosome import Chromosome


class Population:

    def __init__(self, pop_size):
        self.chromosomes = []
        self.size = pop_size
        self.generation = 0
        self.pop_fitness = 0
        self.dir_path = "/home/piotrs/GA/Core+Boron/Generation_"

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

    def best_chromosome(self, fit_or_chrom=0):
        best_fitness = 0.0
        best_dec = 0
        best_keff_nominal = 0.0
        best_keff_void = 0.0
        best_svr = 0.0
        for chromosome in self.chromosomes:
            if best_fitness < chromosome.get_fitness():
                best_fitness = chromosome.get_fitness()
                best_dec = chromosome.chromosome_dec
                best_keff_nominal = chromosome.keff_nominal
                best_keff_void = chromosome.keff_void
                best_svr = (best_keff_void - best_keff_nominal) / (best_keff_void* best_keff_nominal) * 10 ** 5

        if fit_or_chrom == 0:
            return best_fitness
        elif fit_or_chrom == 1:
            return best_dec
        elif fit_or_chrom == 2:
            return best_keff_nominal
        elif fit_or_chrom == 3:
            return best_keff_void
        elif fit_or_chrom == 4:
            return best_svr

    def makedir(self):
        os.mkdir(self.dir_path + str(self.generation))

    def simulation(self):
        counter = 1
        for chromosome in self.chromosomes:
            pattern_nominal = open("/home/piotrs/GA/Core+Boron/input_nominal.inp", "r")
            chromosome_nominal_path = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_nominal" + ".inp"
            chromosome_input_nominal = open(chromosome_nominal_path, "w")
            for line in pattern_nominal:
                if "surf 11 pz" in line:
                    line += str(chromosome.get_lower_position()) + "\n"
                if "surf 12 pz" in line:
                    line += str(chromosome.get_lower_position() + chromosome.get_lower_thickness()) + "\n"
                if "surf 16 pz" in line:
                    line += str(chromosome.get_upper_position()) + "\n"
                if "surf 17 pz" in line:
                    line += str(chromosome.get_upper_position() + chromosome.get_upper_thickness()) + "\n"
                chromosome_input_nominal.write(line)

            pattern_nominal.close()
            chromosome_input_nominal.close()

            bash_path_nominal = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_nominal" + ".sh"
            bash_nominal_input = open(bash_path_nominal, "w")
            bash_cmd = "#!/bin/bash\n/home/piotrs/GA/Core+Boron/sss2 -omp 4 "
            bash_nominal_input.write(bash_cmd + self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_nominal" + ".inp")
            bash_nominal_input.close()

            # print("\nSymulacja dla chromosomu: {} z pokolenia {}".format(chromosome, self.generation))
            os.system("bash " + bash_path_nominal)

            chromosome_nominal_output = open(chromosome_nominal_path + "_res.m", "r")
            for line in chromosome_nominal_output:
                if "ABS_KEFF" in line:
                    chromosome.keff_nominal = float(line[47:58])

            pattern_voided = open("/home/piotrs/GA/Core+Boron/input_void.inp", "r")
            chromosome_voided_path = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_void" + ".inp"
            chromosome_input_voided = open(chromosome_voided_path, "w")
            for line in pattern_voided:
                if "surf 11 pz" in line:
                    line += str(chromosome.get_lower_position()) + "\n"
                if "surf 12 pz" in line:
                    line += str(chromosome.get_lower_position() + chromosome.get_lower_thickness()) + "\n"
                if "surf 16 pz" in line:
                    line += str(chromosome.get_upper_position()) + "\n"
                if "surf 17 pz" in line:
                    line += str(chromosome.get_upper_position() + chromosome.get_upper_thickness()) + "\n"
                chromosome_input_voided.write(line)

            pattern_voided.close()
            chromosome_input_voided.close()

            bash_path_voided = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_void" + ".sh"
            bash_voided_input = open(bash_path_voided, "w")
            bash_cmd = "#!/bin/bash\n/home/piotrs/GA/Core+Boron/sss2 -omp 4 "
            bash_voided_input.write(bash_cmd + self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                chromosome.chromosome_dec) + "_void" + ".inp")
            bash_voided_input.close()

            # print("\nSymulacja dla chromosomu: {} z pokolenia {}".format(chromosome, self.generation))
            os.system("bash " + bash_path_voided)

            chromosome_voided_output = open(chromosome_voided_path + "_res.m", "r")
            for line in chromosome_voided_output:
                if "ABS_KEFF" in line:
                    chromosome.keff_void = float(line[47:58])

            counter += 1
