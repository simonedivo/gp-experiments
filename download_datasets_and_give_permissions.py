import gdown
import os

print("Downloading datasets...")
url = "https://drive.google.com/drive/folders/1Se6O2pFYaHLhfSTwGZXbFJqw4NeUdnNB?usp=sharing"
gdown.download_folder(url)
print("Download complete!")


print("Setting permissions...")
files = ['execute_parallel.sh', 'parallel.sh', 'gpgomea_experiments_no_list.py']
for file in files:
    os.chmod(file, 0o777)
print("Permissions set!")
