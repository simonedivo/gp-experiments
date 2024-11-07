import sys

seed = int(sys.argv[1])
dataset_name = str(sys.argv[2])
training_set_dimension = int(sys.argv[3])
popsize = int(sys.argv[4])
generations = int(sys.argv[5])

string_to_remove = f"{seed},{dataset_name},{training_set_dimension},{popsize},{generations}\n"

with open("btbpg_input_args_updated.txt", "r") as f:
    full_txt = f.read()
    f.close()

modified_txt = full_txt.replace(string_to_remove, "")

with open("btbpg_input_args_updated.txt", "w") as f:
    f.write(modified_txt)
    f.close()
