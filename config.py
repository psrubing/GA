# Simulation settings
num_generations = 50    # number of iterated generations
pop_size = 10           # amount of individuals in population
mutation_prob = 0.05    # mutaion rate (double between 0.0 and 1.0)

# directories and files settings
project_dir = "~/"                                                                             # main project directory path
best_path = project_dir + "Best_Chromosomes.txt"                                               # best from gen file
dir_path = project_dir + "Generation_"                                                         # results folders
serpent_path = project_dir + "sss2"                                                            # serpent file
patterns = [project_dir + "input_nominal.inp", project_dir + "input_void.inp"]                 # serpent inputs
