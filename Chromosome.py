import random
import math

class Chromosome:

    chromosome_length = 32

    def __init__(self,chromosome_list=None):

        if chromosome_list is None:
            self.chromosome_dec = random.randint(0, (2 ** self.chromosome_length) - 1)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
            self.chromosome_list = [int(i) for i in self.chromosome_bin]
        else:
            self.chromosome_list = chromosome_list
            self.chromosome_dec = int("".join(str(x) for x in self.chromosome_list), 2)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
        self.keff = 0

    def get_uranium_radius(self):
        value =  int(self.chromosome_bin[0:16],base=2)
        return 1 + (value * 14.0) / float((2 ** 16) - 1)

    def get_water_radius(self):
        value = int(self.chromosome_bin[16:32],base=2)
        return 15 + (value * 35) / float((2 ** 16) - 1)

    def get_fitness(self):
        dens_uranium = 10.1
        dens_water = 1.0
        vol_uranium = 4.2*(self.get_uranium_radius())**3
        vol_water = 4.2*(self.get_water_radius()-self.get_uranium_radius())**3
        return 1 / (abs(1 - self.keff) * math.sqrt(dens_uranium * vol_uranium + dens_water * vol_water))

    def __str__(self):
        return "Chromosome with {} fitness, uranium radius: {}, water radius: {}, keff: {}, list: {}, dec: {}, bin: {}".format(self.get_fitness(), self.get_uranium_radius(), self.get_water_radius(),
                                                                                                                               self.keff, self.chromosome_list, self.chromosome_dec, self.chromosome_bin)


