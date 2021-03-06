import random


class Chromosome:
    chromosome_length = 111

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

    def get_p3(self):
        value = int(self.chromosome_bin[0:6], base=2)
        return 1 + (value * 68) / float((2 ** 6) - 1)

    def get_p4(self):
        value = int(self.chromosome_bin[6:12], base=2)
        return 5 + self.get_p3() + (value * 45) / float((2 ** 6) - 1)

    def get_p5(self):
        value = int(self.chromosome_bin[12:18], base=2)
        return 1 + (value * 68) / float((2 ** 6) - 1)

    def get_p6(self):
        value = int(self.chromosome_bin[18:24], base=2)
        return 5 + self.get_p5() + (value * 45) / float((2 ** 6) - 1)

    def get_p7(self):
        value = int(self.chromosome_bin[24:30], base=2)
        return 1 + (value * 68) / float((2 ** 6) - 1)

    def get_p8(self):
        value = int(self.chromosome_bin[30:36], base=2)
        return 5 + self.get_p7() + (value * 45) / float((2 ** 6) - 1)

    def get_p11(self):
        value = int(self.chromosome_bin[36:42], base=2)
        return 221.6533 + (value * 39) / float((2 ** 6) - 1)

    def get_p12(self):
        value = int(self.chromosome_bin[42:48], base=2)
        return 5 + self.get_p11() + (value * 45) / float((2 ** 6) - 1)

    def get_p13(self):
        value = int(self.chromosome_bin[48:54], base=2)
        return 221.6533 + (value * 39) / float((2 ** 6) - 1)

    def get_p14(self):
        value = int(self.chromosome_bin[54:60], base=2)
        return 5 + self.get_p13() + (value * 45) / float((2 ** 6) - 1)

    def get_p15(self):
        value = int(self.chromosome_bin[60:66], base=2)
        return 221.6533 + (value * 39) / float((2 ** 6) - 1)

    def get_p16(self):
        value = int(self.chromosome_bin[66:72], base=2)
        return 5 + self.get_p15() + (value * 45) / float((2 ** 6) - 1)

    def get_w4(self):
        value = int(self.chromosome_bin[72:77], base=2)
        return 247 + (value * 20) / float((2 ** 5) - 1)

    def get_w5(self):
        value = int(self.chromosome_bin[77:83], base=2)
        return 5 + self.get_w4() + (value * 45) / float((2 ** 6) - 1)

    def get_enrichment_1(self):
        value = int(self.chromosome_bin[83:87], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_2(self):
        value = int(self.chromosome_bin[87:91], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_3(self):
        value = int(self.chromosome_bin[91:95], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_4(self):
        value = int(self.chromosome_bin[95:99], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_5(self):
        value = int(self.chromosome_bin[99:103], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_6(self):
        value = int(self.chromosome_bin[103:107], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_enrichment_7(self):
        value = int(self.chromosome_bin[107:111], base=2)
        return 0.1 + (value * 0.7) / float((2 ** 4) - 1)

    def get_fitness(self, min_val, generation):

        if generation == 0:
            const = 0
        else:
            const = min_val
        svr = (self.keff_void - self.keff_nominal) / (self.keff_void * self.keff_nominal) * 10 ** 5
        if (self.keff_nominal / svr) - 0.95 * const < 0:
            return abs((self.keff_nominal / svr) - 0.95 * const)
        else:
            return (self.keff_nominal / svr) - 0.95 * const

    def __str__(self):
        return "Chromosome with keff_nominal: {}, keff_voided: {}, list: {}, dec: {}, bin: {}".format(self.keff_nominal,
                                                                                                      self.keff_void,
                                                                                                      self.chromosome_list,
                                                                                                      self.chromosome_dec,
                                                                                                      self.chromosome_bin)
