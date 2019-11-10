import random

class Chromosome:

    chromosome_length = 16

    def __init__(self,chromosome_list=None):

        if chromosome_list is None:
            self.chromosome_dec = random.randint(0, (2 ** 16) - 1)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
            self.chromosome_list = [int(i) for i in self.chromosome_bin]
        else:
            self.chromosome_list = chromosome_list
            self.chromosome_dec = int("".join(str(x) for x in self.chromosome_list), 2)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
        self.keff = 0.0


    def get_variable(self):
        return (self.chromosome_dec*15.75) / float((2 ** 16) - 1)
        # zamienia chromosom na liczbe z przedziału (0,15.75)

    def get_fitness(self):
        sum = 0
        for gene in self.chromosome_list:
            sum += gene
        return sum

    def __str__(self):
        return "Chromosome with {} fitness, variable: {}, list: {}, dec: {}, bin: {}".format(self.get_fitness(), self.get_variable(), self.chromosome_list,
                                                                                             self.chromosome_dec, self.chromosome_bin)



