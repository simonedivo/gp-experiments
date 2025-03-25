Already finished experiment can be found at:
```sh
https://drive.google.com/file/d/1KSFuojpR2vJb4fZkCn9eB0VKK6FRhloC/view?usp=sharing
```
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
git clone https://github.com/simonedivo/gp-experiments
cd gp-experiments
```
After that, if privileges are not set, be sure to give the following permissions:
```sh
chmod 777 *.sh
chmod 777 *.py
```
Then in the conda environment do:
```sh
python3 download_datasets_and_mkdir.py
```
Then just run
```sh
./execute_parallel.sh x y
```
where x is the number of parallel processes to execute concurrently and y the location of the input_args