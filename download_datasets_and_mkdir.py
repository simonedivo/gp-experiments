import gdown
import os

def save_file(str, dir, filename):
    if not os.path.exists(dir):
        os.makedirs(dir)
    full_path = os.path.join(dir, filename)
    with open(full_path, "w") as f:
        f.write(str)
        f.close()

url = "https://drive.google.com/drive/folders/1Se6O2pFYaHLhfSTwGZXbFJqw4NeUdnNB?usp=sharing"
gdown.download_folder(url)

print("Creating folders...")
result_path = 'GPGomea/results'
if not os.path.exists(result_path):
    os.makedirs(result_path)

progress_log_path = 'GPGomea/progress_logs'
if not os.path.exists(progress_log_path):
    os.makedirs(progress_log_path)

finished_runs_path = 'GPGomea/finished_runs'
if not os.path.exists(finished_runs_path):
    os.makedirs(finished_runs_path)

error_runs_path = 'GPGomea/error_runs'
if not os.path.exists(error_runs_path):
    os.makedirs(error_runs_path)

save_file("List of already finished runs \n","GPGomea/finished_runs","finished_runs.txt")
print("Folders created!")


#print("Setting permissions...")
#files = ['execute_parallel.sh', 'parallel.sh', 'gpgomea_experiments_no_list.py']
#for file in files:
#    os.chmod(file, 0o777)
#print("Permissions set!")
