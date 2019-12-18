import random
import os
import subprocess
import multiprocessing

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
        sum_level = 0.0

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
                best_svr = (best_keff_void - best_keff_nominal) / (best_keff_void * best_keff_nominal) * 10 ** 5

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

    def write_input(self, patterns):
        counter = 1
        endings = ["_nominal", "_void"]
        for chromosome in self.chromosomes:
            for i, j in enumerate(patterns):
                pattern = open(j, "r")
                chromosome_path = self.dir_path + str(self.generation) + "/" + str(counter) + "_" + str(
                    chromosome.chromosome_dec) + endings[i]
                chromosome_input = open(chromosome_path + ".inp", "w")
                for line in pattern:
                    if "radial_reflector   p" in line:
                        line = "radial_reflector " + str(chromosome.get_radial_shield_start()) + "\n"
                    if "boron_shield       p" in line:
                        line = "boron_shield " + str(chromosome.get_radial_shield_end()) + "\n"
                    if "surf 11 pz" in line:
                        line += str(chromosome.get_s11()) + "\n"
                    if "surf 12 pz" in line:
                        line += str(chromosome.get_s12()) + "\n"
                    if "surf 13 pz" in line:
                        line += str(chromosome.get_s13()) + "\n"
                    if "surf 14 pz" in line:
                        line += str(chromosome.get_s14()) + "\n"
                    if "surf 15 pz" in line:
                        line += str(chromosome.get_s15()) + "\n"
                    if "surf 16 pz" in line:
                        line += str(chromosome.get_s16()) + "\n"
                    if "surf 19 pz" in line:
                        line += str(chromosome.get_s19()) + "\n"
                    if "surf 20 pz" in line:
                        line += str(chromosome.get_s20()) + "\n"
                    if "surf 21 pz" in line:
                        line += str(chromosome.get_s21()) + "\n"
                    if "surf 22 pz" in line:
                        line += str(chromosome.get_s22()) + "\n"
                    if "surf 23 pz" in line:
                        line += str(chromosome.get_s23()) + "\n"
                    if "surf 24 pz" in line:
                        line += str(chromosome.get_s24()) + "\n"
                    if "cell 3  0 fill " in line:
                        line = "cell 3  0 fill " + str(chromosome.get_first_pin_lower()) + "  11 -12   -27" + "\n"
                    if "cell 5  0 fill " in line:
                        line = "cell 5  0 fill " + str(chromosome.get_second_pin_lower()) + "  13 -14   -27" + "\n"
                    if "cell 7  0 fill " in line:
                        line = "cell 7  0 fill " + str(chromosome.get_third_pin_lower()) + "  15 -16   -27" + "\n"
                    if "cell 11  0 fill " in line:
                        line = "cell 11  0 fill " + str(chromosome.get_first_pin_upper()) + "  19 -20   -27" + "\n"
                    if "cell 13  0 fill " in line:
                        line = "cell 13  0 fill " + str(chromosome.get_second_pin_upper()) + "  21 -22   -27" + "\n"
                    if "cell 15  0 fill " in line:
                        line = "cell 15  0 fill " + str(chromosome.get_third_pin_upper()) + "  23 -24   -27" + "\n"

                    chromosome_input.write(line)

                pattern.close()
                chromosome_input.close()
                if i == 0:
                    chromosome.nominal_path = chromosome_path + ".inp"
                elif i == 1:
                    chromosome.void_path = chromosome_path + ".inp"
            counter += 1

    def simulation_nominal(self):

        for chromosome in self.chromosomes:
            print("\nSymulacja dla chromosomu nominal: {}".format(chromosome.chromosome_dec))
            try:
                subprocess.run(["/home/piotrs/GA/Core+Boron/sss2", "-omp", str(multiprocessing.cpu_count()),
                                chromosome.nominal_path])
            except subprocess.CalledProcessError:
                print("Error")

    def simulation_void(self):

        for chromosome in self.chromosomes:
            print("\nSymulacja dla chromosomu void: {}".format(chromosome.chromosome_dec))
            try:
                subprocess.run(
                    ["/home/piotrs/GA/Core+Boron/sss2", "-omp", str(multiprocessing.cpu_count()), chromosome.void_path])
            except subprocess.CalledProcessError:
                print("Error")

    def get_k_nominal(self):
        for chromosome in self.chromosomes:
            chromosome_nominal_output = open(chromosome.nominal_path + "_res.m", "r")
            for line in chromosome_nominal_output:
                if "ABS_KEFF" in line:
                    chromosome.keff_nominal = float(line[47:58])

    def get_k_void(self):
        for chromosome in self.chromosomes:
            chromosome_void_output = open(chromosome.void_path + "_res.m", "r")
            for line in chromosome_void_output:
                if "ABS_KEFF" in line:
                    chromosome.keff_void = float(line[47:58])
