import sys
import threading

seed = int(sys.argv[1])
dataset_name = str(sys.argv[2])
training_set_dimension = int(sys.argv[3])
popsize = int(sys.argv[4])
generations = int(sys.argv[5])
txt_to_update = str(sys.argv[6])

lock = threading.Lock()
string_to_remove = f"{seed},{dataset_name},{training_set_dimension},{popsize},{generations}\n"

with lock:
    with open(txt_to_update, "r") as f:
        full_txt = f.read()
        f.close()

    modified_txt = full_txt.replace(string_to_remove, "")

    with open(txt_to_update, "w") as f:
        f.write(modified_txt)
        f.close()
