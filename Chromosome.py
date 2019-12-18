import random


class Chromosome:
    chromosome_length = 128

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

    def get_s11(self):
        value = int(self.chromosome_bin[0:8], base=2)
        return 5 + (value * 85) / float((2 ** 8) - 1)

    def get_s12(self):
        value = int(self.chromosome_bin[8:16], base=2)
        return 5 + self.get_s11() + (value * (90 - self.get_s11())) / float((2 ** 8) - 1)

    def get_s13(self):
        value = int(self.chromosome_bin[16:24], base=2)
        return 5 + self.get_s12() + (value * (95 - self.get_s12())) / float((2 ** 8) - 1)

    def get_s14(self):
        value = int(self.chromosome_bin[24:32], base=2)
        return 5 + self.get_s13() + (value * (100 - self.get_s13())) / float((2 ** 8) - 1)

    def get_s15(self):
        value = int(self.chromosome_bin[32:40], base=2)
        return 5 + self.get_s14() + (value * (105 - self.get_s14())) / float((2 ** 8) - 1)

    def get_s16(self):
        value = int(self.chromosome_bin[40:48], base=2)
        return 5 + self.get_s15() + (value * (110 - self.get_s15())) / float((2 ** 8) - 1)

    def get_s19(self):
        value = int(self.chromosome_bin[48:56], base=2)
        return 225.6533 + (value * 55) / float((2 ** 8) - 1)

    def get_s20(self):
        value = int(self.chromosome_bin[56:64], base=2)
        return 5 + self.get_s19() + (value * (280 - self.get_s19())) / float((2 ** 8) - 1)

    def get_s21(self):
        value = int(self.chromosome_bin[64:72], base=2)
        return 5 + self.get_s20() + (value * (285 - self.get_s20())) / float((2 ** 8) - 1)

    def get_s22(self):
        value = int(self.chromosome_bin[72:80], base=2)
        return 5 + self.get_s21() + (value * (290 - self.get_s21())) / float((2 ** 8) - 1)

    def get_s23(self):
        value = int(self.chromosome_bin[80:88], base=2)
        return 5 + self.get_s22() + (value * (295 - self.get_s22())) / float((2 ** 8) - 1)

    def get_s24(self):
        value = int(self.chromosome_bin[88:96], base=2)
        return 5 + self.get_s23() + (value * (300 - self.get_s23())) / float((2 ** 8) - 1)

    def get_radial_shield_start(self):
        value = int(self.chromosome_bin[96:103], base=2)
        return 250 + (value * 55) / float((2 ** 7) - 1)

    def get_radial_shield_end(self):
        value = int(self.chromosome_bin[103:110], base=2)
        return 5 + self.get_radial_shield_start() + (value * (305 - self.get_radial_shield_start())) / float(
            (2 ** 7) - 1)

    def get_first_pin_lower(self):
        value = int(self.chromosome_bin[110:113], base=2)
        if value == 1:
            return 5
        elif value == 2:
            return 6
        elif value == 3:
            return 7
        elif value == 4:
            return 8
        elif value == 5:
            return 9
        elif value == 6:
            return 10
        elif value == 7:
            return 11
        else:
            return 2

    def get_second_pin_lower(self):
        value = int(self.chromosome_bin[113:116], base=2)
        if value == 1:
            return 5
        elif value == 2:
            return 6
        elif value == 3:
            return 7
        elif value == 4:
            return 8
        elif value == 5:
            return 9
        elif value == 6:
            return 10
        elif value == 7:
            return 11
        else:
            return 2

    def get_third_pin_lower(self):
        value = int(self.chromosome_bin[116:119], base=2)
        if value == 1:
            return 5
        elif value == 2:
            return 6
        elif value == 3:
            return 7
        elif value == 4:
            return 8
        elif value == 5:
            return 9
        elif value == 6:
            return 10
        elif value == 7:
            return 11
        else:
            return 2

    def get_first_pin_upper(self):
        value = int(self.chromosome_bin[119:122], base=2)
        if value == 1:
            return 12
        elif value == 2:
            return 13
        elif value == 3:
            return 14
        elif value == 4:
            return 15
        elif value == 5:
            return 16
        elif value == 6:
            return 17
        else:
            return 3

    def get_second_pin_upper(self):
        value = int(self.chromosome_bin[122:125], base=2)
        if value == 1:
            return 12
        elif value == 2:
            return 13
        elif value == 3:
            return 14
        elif value == 4:
            return 15
        elif value == 5:
            return 16
        elif value == 6:
            return 17
        else:
            return 3

    def get_third_pin_upper(self):
        value = int(self.chromosome_bin[125:128], base=2)
        if value == 1:
            return 12
        elif value == 2:
            return 13
        elif value == 3:
            return 14
        elif value == 4:
            return 15
        elif value == 5:
            return 16
        elif value == 6:
            return 17
        else:
            return 3

    def get_fitness(self):
        # svr = (self.keff_voided - self.keff_nominal) / (self.keff_voided * self.keff_nominal) * 10 ** 5
        # f_k = 1000 * (0.03 + self.keff_nominal - self.keff_void)
        # barrier = 0.05
        # if f_k < barrier:
        # return barrier
        # else:
        # return f_k
        return self.keff_nominal ** 60 / self.keff_void ** 80

    def __str__(self):
        return "Chromosome with {} fitness, keff_nominal: {}, keff_voided: {}, list: {}, dec: {}, bin: {}".format(
            self.get_fitness(), self.keff_nominal, self.keff_void, self.chromosome_list, self.chromosome_dec,
            self.chromosome_bin)
