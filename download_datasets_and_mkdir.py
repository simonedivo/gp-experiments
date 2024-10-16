import gdown
import os

print("Downloading datasets...")
url = "https://drive.google.com/drive/folders/1Se6O2pFYaHLhfSTwGZXbFJqw4NeUdnNB?usp=sharing"
gdown.download_folder(url)
print("Download complete!")

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
print("Folders created!")


#print("Setting permissions...")
#files = ['execute_parallel.sh', 'parallel.sh', 'gpgomea_experiments_no_list.py']
#for file in files:
#    os.chmod(file, 0o777)
#print("Permissions set!")
