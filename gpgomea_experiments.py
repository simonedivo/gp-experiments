import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime
import random
from pyGPGOMEA import GPGOMEARegressor as GPGR
import os
import sys

def main():
    #datasets_folder = './datasets/'
    #datasets = ['1191_BNG_pbc.tsv', '1196_BNG_pharynx.tsv', '1595_poker.tsv']
    #n_seeds = 2
    #training_set_dimension_list = [100, 1000]
    #popsize_generations_list = [[10,10], [100, 10]]
    result_path = 'GPGomea/results'
    create_folder(result_path)
    datasets_folder = './datasets/'

    seed = int(sys.argv[1])
    dataset_name = str(sys.argv[2])

    training_set_dimension_list = sys.argv[3].split("/")
    for i in range(len(training_set_dimension_list)):
        training_set_dimension_list[i] = int(training_set_dimension_list[i])

    pgl = sys.argv[4]
    popsize_generations_list = [string.split('/') for string in pgl.split('|')]
    for i in range(len(popsize_generations_list)):
        for j in range(len(popsize_generations_list[i])):
            popsize_generations_list[i][j] = int(popsize_generations_list[i][j])
    
    #print(seed, dataset_name, training_set_dimension_list, popsize_generations_list)

    all_in_one(datasets_folder, dataset_name, result_path, seed, training_set_dimension_list, popsize_generations_list)


def save_file(str, dir, filename):
    if not os.path.exists(dir):
        os.makedirs(dir)
    full_path = os.path.join(dir, filename)
    with open(full_path, "w") as f:
        f.write(str)

def generate_random_seeds(n_seeds):
    list_of_numbers = list(range(0, 1000000))
    random_seeds = random.sample(list_of_numbers, n_seeds)
    save_file(str(random_seeds), 'GPGomea/random_seeds', 'random_seeds.txt')
    return random_seeds

def seeded_training_set_dimension(dataset, dimension, seed):
    return dataset.sample(n=dimension, random_state=seed)

def seeded_custom_dataset_creator(X_train, y_train, train_dimension, seed):

    if(train_dimension >= X_train.shape[0]):
        X_train.to_numpy()
        y_train.to_numpy()
        return X_train.values, y_train.values
        #return X_train, y_train

    X_train_subset = seeded_training_set_dimension(X_train, train_dimension, seed)
    y_train_subset = seeded_training_set_dimension(y_train, train_dimension, seed)

    X_train_subset.to_numpy()
    y_train_subset.to_numpy()
    
    return X_train_subset.values, y_train_subset.values
    #return X_train_subset, y_train_subset

def GPGR_custom_starter(X_train, X_test, y_train, y_test, popsize, generations, seed):
    ea = GPGR( 
    	gomea=False,
    	functions="+_-_*_p/",
    	time=-1, generations=generations, evaluations=-1,
        subcross=0.8, submut=0.4,
        elitism=1,
    	initmaxtreeheight=4,
        maxtreeheight=12,
    	ims=False,
    	popsize=popsize,
    	parallel=False,
    	linearscaling=True,
        seed=seed,
        caching=False,
        logtofile=False,
    	silent=True)
    starting_time = datetime.now()
    ea.fit(X_train, y_train)
    ending_time = datetime.now()
    # get the model and change some operators such as protected division and protected log to be sympy-digestible
    model = ea.get_model().replace("p/","/").replace("plog","log")
    # let's also call vars with their names
    #model = str(sympy.simplify(model))
    #model = model.replace("x0","mass1").replace("x1","mass2").replace("x2","dist")
    # sometimes due to numerical precision, sympy might be unable to do this
    #if model == "0":
    #    print("Warning: sympy couldn't make it due to numerical precision")
    #    model = ea.get_model().replace("p/","/").replace("plog","log").replace("x0","mass1").replace("x1","mass2").replace("x2","dist") # re-set to non-simplified model
    #print('Model found:', model)
    #print('Evaluations taken:', ea.get_evaluations()) # care: this is not correct if multiple threads were used when fitting
    test_rmse = np.sqrt( mean_squared_error(y_test, ea.predict(X_test)) )
    train_rmse = np.sqrt( mean_squared_error(y_train, ea.predict(X_train)) )
    #print('Test RMSE:', test_rmse)
    #print('Train RMSE:', train_rmse)
    final_population = ea.get_final_population(X_train)
    n_nodes = ea.get_n_nodes()
    evaluations = ea.get_evaluations()
    progress_log = ea.get_progress_log()
    #print("Progress log:", progress_log)
    time_taken = ending_time - starting_time
    #print("Time taken for this iteration:", time_taken)
    #print("\n")

    #quit()
    return model, final_population, n_nodes, evaluations, progress_log, test_rmse, train_rmse, time_taken

def seeded_grid_search(dataset_name, X_train, X_test, y_train, y_test, training_set_dimension_list, popsize_generations_list, seed):
    #print("Starting date & time: ", datetime.now())
    i = 0
    lst = []

    for training_set_dimension in training_set_dimension_list:
        X_train_subset, y_train_subset = seeded_custom_dataset_creator(X_train, y_train, training_set_dimension, seed)
        for popsize, generations in popsize_generations_list:
            #print("Iteration: ", i)
            i+=1
            #print("Training set dimension: ", training_set_dimension, "Popsize: ", popsize, "Generations: ", generations)
            model, final_population, n_nodes, evaluations, progress_log, test_rsme, train_rmse, time_taken = GPGR_custom_starter(X_train_subset, X_test, y_train_subset, y_test, popsize, generations, seed)
            lst.append([training_set_dimension, popsize, generations, test_rsme, train_rmse, time_taken, model, final_population, n_nodes, evaluations])
            save_file(progress_log, "GPGomea/progress_logs", "progress_log_"+ dataset_name + "_train_dim_" + str(training_set_dimension) + "_popsize_" + str(popsize) + "_generations_" + str(generations) + ".csv")
                
    
    #print("Ending date & time: ", datetime.now())
    results = pd.DataFrame(lst, columns=['training_set_dimension', 'popsize', 'generations', 'test_rmse', 'train_rmse', 'time_taken', 'model', 'final_population', 'n_nodes', 'evaluations'])
    return results

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def all_in_one(datasets_folder, dataset_name, result_path,seed, training_set_dimension_list, popsize_generations_list):

    dataset_path = os.path.join(datasets_folder, dataset_name)
    
    if("csv" in dataset_path):
        dataset = pd.read_csv(dataset_path)
    if("tsv" in dataset_path):
        dataset = pd.read_csv(dataset_path, sep='\t')
    
    dataset.dropna(inplace=True)
    X = dataset.drop(columns=['target'])
    y = dataset['target']
    #print("Currently working on " + dataset_path + " with seed " + str(seed))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=seed, shuffle=True)
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()
    results = seeded_grid_search(dataset_name, X_train, X_test, y_train, y_test, training_set_dimension_list, popsize_generations_list, seed)
    results.to_csv( os.path.join(result_path,'results_of_' + dataset_name + '_seed_' + str(seed) + '.csv'), index=False)
        

if __name__ == '__main__':
    main()