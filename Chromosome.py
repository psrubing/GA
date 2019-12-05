import random


class Chromosome:
    chromosome_length = 64

    def __init__(self, chromosome_list=None):

        if chromosome_list is None:
            self.chromosome_dec = random.randint(0, (2 ** self.chromosome_length) - 1)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
            self.chromosome_list = [int(i) for i in self.chromosome_bin]
        else:
            self.chromosome_list = chromosome_list
            self.chromosome_dec = int("".join(str(x) for x in self.chromosome_list), 2)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
        self.keff_nominal = 0.0
        self.keff_voided = 0.0

    # def get_uranium_radius(self):
    #    value = int(self.chromosome_bin[0:16], base=2)
    #    return 1 + (value * 10.0) / float((2 ** 16) - 1)

    # def get_water_radius(self):
    #    value = int(self.chromosome_bin[16:32], base=2)
    #    return 9 + (value * 33) / float((2 ** 16) - 1)

    def get_lower_thickness(self):
        value = int(self.chromosome_bin[0:16], base=2)
        return 0.1 + (value * 86.8175) / float((2 ** 16) - 1)

    def get_lower_position(self):
        value = int(self.chromosome_bin[16:32], base=2)
        return 1.0 + (value * (87.9175 - self.get_lower_thickness())) / float((2 ** 16) - 1)

    def get_upper_thickness(self):
        value = int(self.chromosome_bin[32:48], base=2)
        return 0.1 + (value * 6.9566) / float((2 ** 16) - 1)

    def get_upper_position(self):
        value = int(self.chromosome_bin[48:64], base=2)
        return 221.6533 + (value * (8.0566 - self.get_upper_thickness())) / float((2 ** 16) - 1)

    def get_enrichment(self):
        value = int(self.chromosome_bin[0:16], base=2)
        return 1 + (value * 10.0) / float((2 ** 16) - 1)

    def get_fitness(self):
        # dens_uranium = 19.1
        # dens_water = 1.0
        # vol_uranium = 4.2 * (self.get_uranium_radius()) ** 3
        # vol_water = 4.2 * (self.get_water_radius() - self.get_uranium_radius()) ** 3
        # return (100 * math.exp(-20.0 * abs(1 - self.keff_nominal))) / (dens_uranium * vol_uranium + dens_water * vol_water)
        # return (0.1 / (abs(self.keff - 1) ** 6)) / (dens_uranium * vol_uranium + dens_water * vol_water)
        svr = (self.keff_voided - self.keff_nominal) / (self.keff_voided * self.keff_nominal) * 10 ** 5
        return 1000 * self.keff_nominal ** 50 / svr

    def __str__(self):
        return "Chromosome with {} fitness, keff_nominal: {}, keff_voided: {}, list: {}, dec: {}, bin: {}".format(
            self.get_fitness(), self.keff_nominal, self.keff_voided, self.chromosome_list, self.chromosome_dec,
            self.chromosome_bin)
