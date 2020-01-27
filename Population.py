import random
import os
import subprocess
import multiprocessing

from Chromosome import Chromosome
import config


class Population:

    def __init__(self, pop_size):
        self.chromosomes = []
        self.size = pop_size
        self.generation = 0
        self.pop_fitness = 0
        self.dir_path = config.dir_path

    def make_population(self):

        for i in range(self.size):
            self.chromosomes.append(Chromosome())

    def calc_pop_fitness(self, min_val, generation):

        for chromosome in self.chromosomes:
            self.pop_fitness += chromosome.get_fitness(min_val, generation)
        return self.pop_fitness

    def roulette(self, min_val, generation):

        pick = random.uniform(0, self.pop_fitness)
        sum_level = 0.0

        for chromosome in self.chromosomes:
            sum_level += chromosome.get_fitness(min_val, generation)
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

    def best_chromosome(self, option, min_val, generation):
        best_fitness = 0.0
        best_dec = 0
        best_keff_nominal = 0.0
        best_keff_void = 0.0
        best_svr = 0.0
        for chromosome in self.chromosomes:
            if best_fitness < chromosome.get_fitness(min_val, generation):
                best_fitness = chromosome.get_fitness(min_val, generation)
                best_dec = chromosome.chromosome_dec
                best_keff_nominal = chromosome.keff_nominal
                best_keff_void = chromosome.keff_void
                best_svr = (best_keff_void - best_keff_nominal) / (best_keff_void * best_keff_nominal) * 10 ** 5

        if option == 0:
            return best_fitness
        elif option == 1:
            return best_dec
        elif option == 2:
            return best_keff_nominal
        elif option == 3:
            return best_keff_void
        elif option == 4:
            return best_svr

    def worst_chromosome(self):
        worst_fitness = 10000000.0
        for chromosome in self.chromosomes:
            if worst_fitness > chromosome.get_fitness(0, 0):
                worst_fitness = chromosome.get_fitness(0, 0)
        return worst_fitness

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

                    if "surf p3 pz" in line:
                        line += str(chromosome.get_p3()) + "\n"
                    if "surf p4 pz" in line:
                        line += str(chromosome.get_p4()) + "\n"
                    if "surf p5 pz" in line:
                        line += str(chromosome.get_p5()) + "\n"
                    if "surf p6 pz" in line:
                        line += str(chromosome.get_p6()) + "\n"
                    if "surf p7 pz" in line:
                        line += str(chromosome.get_p7()) + "\n"
                    if "surf p8 pz" in line:
                        line += str(chromosome.get_p8()) + "\n"
                    if "surf p11 pz" in line:
                        line += str(chromosome.get_p11()) + "\n"
                    if "surf p12 pz" in line:
                        line += str(chromosome.get_p12()) + "\n"
                    if "surf p13 pz" in line:
                        line += str(chromosome.get_p13()) + "\n"
                    if "surf p14 pz" in line:
                        line += str(chromosome.get_p14()) + "\n"
                    if "surf p15 pz" in line:
                        line += str(chromosome.get_p15()) + "\n"
                    if "surf p16 pz" in line:
                        line += str(chromosome.get_p16()) + "\n"
                    if "surf w4 cylz 0.0 0.0" in line:
                        line += str(chromosome.get_w4()) + "\n"
                    if "surf w5 cylz 0.0 0.0" in line:
                        line += str(chromosome.get_w5()) + "\n"
                    if "5010.06c e1" in line:
                        val = 0.03122344
                        line = "5010.06c " + str(val * chromosome.get_enrichment_1()) + "\n"
                    if "5011.06c e1" in line:
                        val = 0.03122344
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_1()) * val) + "\n"
                    if "5010.06c e2" in line:
                        val = 0.03122344
                        line = "5010.06c " + str(val * chromosome.get_enrichment_2()) + "\n"
                    if "5011.06c e2" in line:
                        val = 0.03122344
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_2()) * val) + "\n"
                    if "5010.06c e3" in line:
                        val = 0.03122344
                        line = "5010.06c " + str(val * chromosome.get_enrichment_3()) + "\n"
                    if "5011.06c e3" in line:
                        val = 0.03122344
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_3()) * val) + "\n"
                    if "5010.06c e4" in line:
                        val = 0.0235362797
                        line = "5010.06c " + str(val * chromosome.get_enrichment_4()) + "\n"
                    if "5011.06c e4" in line:
                        val = 0.0235362797
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_4()) * val) + "\n"
                    if "5010.06c e5" in line:
                        val = 0.0235362797
                        line = "5010.06c " + str(val * chromosome.get_enrichment_5()) + "\n"
                    if "5011.06c e5" in line:
                        val = 0.0235362797
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_5()) * val) + "\n"
                    if "5010.06c e6" in line:
                        val = 0.0235362797
                        line = "5010.06c " + str(val * chromosome.get_enrichment_6()) + "\n"
                    if "5011.06c e6" in line:
                        val = 0.0235362797
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_6()) * val) + "\n"
                    if "5010.06c e7" in line:
                        val = 0.013121174466
                        line = "5010.06c " + str(val * chromosome.get_enrichment_7()) + "\n"
                    if "5011.06c e7" in line:
                        val = 0.013121174466
                        line = "5011.06c " + str((1 - chromosome.get_enrichment_7()) * val) + "\n"

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
                subprocess.run(
                    [config.serpent_path, "-omp", str(multiprocessing.cpu_count()), chromosome.nominal_path])
            except subprocess.CalledProcessError:
                print("Error")

    def simulation_void(self):

        for chromosome in self.chromosomes:
            print("\nSymulacja dla chromosomu void: {}".format(chromosome.chromosome_dec))
            try:
                subprocess.run(
                    [config.serpent_path, "-omp", str(multiprocessing.cpu_count()), chromosome.void_path])
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

    def write_output(self, mode, lowest):

        if mode == 0:
            best_input = open(config.best_path, "w+")
            best_input.write(
                "Generation\tPopulation Fitness\tBest Chromosome Fitness\t\tBest Chromosome\t\tkeff_nominal\t\tkeff_void\t\tSVR\n")
            best_input.write(
                str(self.generation) + "\t\t" + str(self.pop_fitness) + "\t" + str(
                    self.best_chromosome(0, lowest, self.generation)) + "\t\t" + str(
                    self.best_chromosome(1, lowest, self.generation))
                + "\t\t" + str(self.best_chromosome(2, lowest, self.generation)) + "\t\t\t" + str(
                    self.best_chromosome(3, lowest, self.generation)) + "\t\t" + str(
                    self.best_chromosome(4, lowest, self.generation)) + "\n")
            best_input.close()
        if mode == 1:
            best_input = open(config.best_path, "a+")
            best_input.write(
                str(self.generation) + "\t\t" + str(self.pop_fitness) + "\t" + str(
                    self.best_chromosome(0, lowest, self.generation)) + "\t\t" + str(
                    self.best_chromosome(1, lowest, self.generation))
                + "\t\t" + str(self.best_chromosome(2, lowest, self.generation)) + "\t\t\t" + str(
                    self.best_chromosome(3, lowest, self.generation)) + "\t\t" + str(
                    self.best_chromosome(4, lowest, self.generation)) + "\n")
            best_input.close()
