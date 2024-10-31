import sys

seed = int(sys.argv[1])
dataset_name = str(sys.argv[2])
training_set_dimension = int(sys.argv[3])
popsize = int(sys.argv[4])
generations = int(sys.argv[5])

with open("new_random_seed_copy.txt", "w") as f:
    f.write(str(seed))
    f.close()
