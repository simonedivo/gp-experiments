To run it do:
```sh
git clone https://github.com/simonedivo/GP-GOMEA
cd GP-GOMEA
conda env create -f environment.yml
conda activate gpgomenv-sd
make
```
Then clone this repository and enter inside the folder:
```sh
git clone github.com/simonedivo/gp-experiments
cd gp-experiments
```
Then in the conda environment do:
```sh
download_datasets.py
```
After that, if privileges are not set, be sure to give the following permissions:
```sh
chmod 777 execute_parallel.sh
chmod 777 parallel.sh
chmod 777 gpgomea_experiments_no_list.py
```
Then just run
```sh
./execute_parallel.sh x
```
where x is the number of parallel processes to execute concurrently