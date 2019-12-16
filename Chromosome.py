import random


class Chromosome:
    chromosome_length = 56

    def __init__(self, chromosome_list=None):

        if chromosome_list is None:
            self.chromosome_dec = random.randint(0, (2 ** self.chromosome_length) - 1)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
            self.chromosome_list = [int(i) for i in self.chromosome_bin]
        else:
            self.chromosome_list = chromosome_list
            self.chromosome_dec = int("".join(str(x) for x in self.chromosome_list), 2)
            self.chromosome_bin = bin(self.chromosome_dec)[2:].zfill(self.chromosome_length)
        self.nominal_path = ""
        self.void_path = ""
        self.keff_nominal = 0.0
        self.keff_void = 0.0

    def get_lower_thickness(self):
        value = int(self.chromosome_bin[0:16], base=2)
        return 0.1 + (value * 86.8175) / float((2 ** 16) - 1)

    def get_lower_position(self):
        value = int(self.chromosome_bin[16:32], base=2)
        return 1.0 + (value * (87.9175 - self.get_lower_thickness())) / float((2 ** 16) - 1)

    def get_upper_thickness(self):
        value = int(self.chromosome_bin[32:40], base=2)
        return 0.1 + (value * 6.9566) / float((2 ** 8) - 1)

    def get_upper_position(self):
        value = int(self.chromosome_bin[40:48], base=2)
        return 221.6533 + (value * (8.0566 - self.get_upper_thickness())) / float((2 ** 8) - 1)

    def get_enrichment(self):
        value = int(self.chromosome_bin[48:56], base=2)
        return 0.05 + (value * 0.25) / float((2 ** 8) - 1)

    def get_fitness(self):
        # svr = (self.keff_voided - self.keff_nominal) / (self.keff_voided * self.keff_nominal) * 10 ** 5
        # return 1000 * self.keff_nominal ** 50 / svr
        f_k = 1000 * (0.03 + self.keff_nominal - self.keff_void)
        barrier = 0.05
        if f_k < barrier:
            return barrier
        else:
            return f_k

    def __str__(self):
        return "Chromosome with {} fitness, keff_nominal: {}, keff_voided: {}, list: {}, dec: {}, bin: {}".format(
            self.get_fitness(), self.keff_nominal, self.keff_void, self.chromosome_list, self.chromosome_dec,
            self.chromosome_bin)
