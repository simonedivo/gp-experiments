import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import datetime
from pyGPGOMEA import GPGOMEARegressor as GPGR
import os
import sys
import random

def main():
    result_path = 'GPGomea/results'
    create_folder(result_path)
    create_folder("GPGomea/progress_logs")
    save_file("List of already finished runs \n","GPGomea/finished_runs","finished_runs.txt")
    datasets_folder = './datasets/'

    seed = int(sys.argv[1])
    dataset_name = str(sys.argv[2])

    training_set_dimension = int(sys.argv[3])
    popsize = int(sys.argv[4])
    generations = int(sys.argv[5])
    
    #print(seed, dataset_name, training_set_dimension_list, popsize_generations_list)

    all_in_one_no_list(datasets_folder, dataset_name, result_path, seed, training_set_dimension, popsize, generations)

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_file(str, dir, filename):
    if not os.path.exists(dir):
        os.makedirs(dir)
    full_path = os.path.join(dir, filename)
    with open(full_path, "w") as f:
        f.write(str)

def update_file(str, dir, filename):
    full_path = os.path.join(dir, filename)
    with open(full_path, "a") as f:
        f.write(str)

def training_set_dimension(dataset, dimension, random_seed):
    return dataset.sample(n=dimension, random_state=random_seed)

def custom_dataset_creator(X_train, y_train, train_dimension):

    if(train_dimension >= X_train.shape[0]):
        X_train.to_numpy()
        y_train.to_numpy()
        return X_train.values, y_train.values
        #return X_train, y_train

    random_seed = random.randint(0, 1000000)

    X_train_subset = training_set_dimension(X_train, train_dimension, random_seed)
    y_train_subset = training_set_dimension(y_train, train_dimension, random_seed)

    X_train_subset.to_numpy()
    y_train_subset.to_numpy()
    
    return X_train_subset.values, y_train_subset.values
    #return X_train_subset, y_train_subset

#Questo prenderebbe in input il seed della run e lo utilizzerebbe per fare il sample del training set -> il training set incrementale avrà sempre gli elementi di quelli prima
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
    	gomea=False,gomfos='LT',
    	functions="+_-_*_p/",
    	time=-1, generations=generations, evaluations=-1,
        linearscaling=True,prob="symbreg",multiobj=False,
        erc=True,classweights=False,
        subcross=0.8,submut=0.4,reproduction=0.0,
        sblibtype=False,sbrdo=0.0,sbagx=0.0,
        unifdepthvar=True,tournament=4,elitism=1,
    	initmaxtreeheight=4,inittype=False,
        maxtreeheight=8,maxsize=1000,
    	ims=False,syntuniqinit=1000,
    	popsize=popsize,
        validation=False,
        coeffmut=False,
        gomcoeffmutstrat=False,
        batchsize=False,
        seed=seed,
        parallel=False,
        caching=False,
        logtofile=False,
    	silent=True)
    starting_time = datetime.now()
    ea.fit(X_train, y_train)
    ending_time = datetime.now()
    # get the model and change some operators such as protected division and protected log to be sympy-digestible
    #model = ea.get_model().replace("p/","/").replace("plog","log")
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
    #final_population = ea.get_final_population(X_train)
    n_nodes = ea.get_n_nodes()
    evaluations = ea.get_evaluations()
    progress_log = ea.get_progress_log()
    #print("Progress log:", progress_log)
    time_taken = ending_time - starting_time
    #print("Time taken for this iteration:", time_taken)
    #print("\n")

    #quit()
    return n_nodes, evaluations, progress_log, test_rmse, train_rmse, time_taken

def seeded_grid_search_no_list(dataset_name, X_train, X_test, y_train, y_test, training_set_dimension, popsize, generations, seed):
    lst = []
    X_train_subset, y_train_subset = custom_dataset_creator(X_train, y_train, training_set_dimension) #training set sample may change for each iteration
    n_nodes, evaluations, progress_log, test_rsme, train_rmse, time_taken = GPGR_custom_starter(X_train_subset, X_test, y_train_subset, y_test, popsize, generations, seed)
    lst.append([training_set_dimension, popsize, generations, test_rsme.round(3), train_rmse.round(3), time_taken, n_nodes, evaluations])
    save_file(progress_log, "GPGomea/progress_logs", "progress_log_"+ dataset_name + "_seed_" + str(seed) +  "_train_dim_" + str(training_set_dimension) + "_popsize_" + str(popsize) + "_generations_" + str(generations) + ".csv")

    results = pd.DataFrame(lst, columns=['training_set_dimension', 'popsize', 'generations', 'test_rmse', 'train_rmse', 'time_taken', 'n_nodes', 'evaluations'])
    results['time_taken'] = results['time_taken'].dt.total_seconds()
    return results

def all_in_one_no_list(datasets_folder, dataset_name, result_path, seed, training_set_dimension, popsize, generations):

    dataset_path = os.path.join(datasets_folder, dataset_name)
    
    if("csv" in dataset_path):
        dataset = pd.read_csv(dataset_path)
        dataset_name = dataset_name.replace(".csv", "")
    if("tsv" in dataset_path):
        dataset = pd.read_csv(dataset_path, sep='\t')
        dataset_name = dataset_name.replace(".tsv", "")

    
    dataset.dropna(inplace=True)
    X = dataset.drop(columns=['target'])
    y = dataset['target']
    #print("Currently working on " + dataset_path + " with seed " + str(seed))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42, shuffle=True) #random_state always 42 to keep the same split for all seeds
    X_test = X_test.to_numpy()
    y_test = y_test.to_numpy()
    results = seeded_grid_search_no_list(dataset_name, X_train, X_test, y_train, y_test, training_set_dimension, popsize, generations, seed)
    results.to_csv( os.path.join(result_path,'results_of_' + dataset_name + '_seed_' + str(seed) + '_training_set_dimension' + str(training_set_dimension) + '_popsize_' + str(popsize) + '_generations_' + str(generations) + '.csv'), index=False)
    update_file(dataset_name + "_seed_" + str(seed) + "_training_set_dimension_" + str(training_set_dimension) + "_popsize_" + str(popsize) + "_generations_" + str(generations) + "\n", "GPGomea/finished_runs", "finished_runs.txt")
        

if __name__ == '__main__':
    main()