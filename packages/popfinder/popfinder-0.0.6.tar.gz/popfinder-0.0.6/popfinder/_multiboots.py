import pandas as pd
import numpy as np
import multiprocessing as mp
import argparse
import os

from popfinder.dataloader import GeneticData
from popfinder.classifier import PopClassifier
# from popfinder.regressor import PopRegressor

def _train_on_bootstraps(arg_list):

    popfinder_path, nboots, epochs, valid_size, cv_splits, cv_reps, learning_rate, batch_size, dropout_prop, rep = arg_list
    test_results_final = pd.DataFrame({"bootstrap": [], "sampleID": [], "pop": [], "x": [],
                                    "y": [], "x_pred": [], "y_pred": []})
    pred_results_final = pd.DataFrame({"bootstrap": [], "sampleID": [], "pop": [], 
                                    "x_pred": [], "y_pred": []})   
    for boot in range(nboots):

        popfinder = PopClassifier.load(os.path.join(popfinder_path, "classifier.pkl"))
        popfinder.output_folder = os.path.join(popfinder_path, "rep{}".format(rep))
        os.makedirs(popfinder.output_folder, exist_ok=True)

        # Use bootstrap to randomly select sites from training/test/unknown data
        num_sites = popfinder.data.train["alleles"].values[0].shape[0]

        site_indices = np.random.choice(range(num_sites), size=num_sites,
                                        replace=True)

        popfinder.__boot_data = GeneticData()
        popfinder.__boot_data.train = popfinder.data.train.copy()
        popfinder.__boot_data.test = popfinder.data.test.copy()
        popfinder.__boot_data.knowns = pd.concat([popfinder.data.train, popfinder.data.test])
        popfinder.__boot_data.unknowns = popfinder.data.unknowns.copy()

        # Slice datasets by site_indices
        popfinder.__boot_data.train["alleles"] = [a[site_indices] for a in popfinder.data.train["alleles"].values]
        popfinder.__boot_data.test["alleles"] = [a[site_indices] for a in popfinder.data.test["alleles"].values]
        popfinder.__boot_data.unknowns["alleles"] = [a[site_indices] for a in popfinder.data.unknowns["alleles"].values]

        # Train on new training set
        popfinder.data
        popfinder.train(epochs=epochs, valid_size=valid_size,
                cv_splits=cv_splits, cv_reps=cv_reps,
                learning_rate=learning_rate, batch_size=batch_size,
                dropout_prop=dropout_prop)
        popfinder.test()
        test_locs = popfinder.test_results.copy()
        # test_locs["sampleID"] = test_locs.index
        test_locs["bootstrap"] = boot

        if popfinder.data.unknowns.shape[0] > 0:

            pred_locs = popfinder.assign_unknown(save=False)
            pred_locs["bootstrap"] = boot
            pred_results_final = pd.concat([pred_results_final,
                pred_locs[["bootstrap", "sampleID", "true_pop", "pred_pop"]]])

        # test_results_final = pd.concat([test_results_final,
        #     test_locs[["bootstrap", "sampleID", "pop", "x", "y", "x_pred", "y_pred"]]])
        test_results_final = pd.concat([test_results_final,
                                        test_locs[["bootstrap", "true_pop", "pred_pop"]]])
        
    return test_results_final, pred_results_final


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="Path to PopClassifier object")
    parser.add_argument("-n", help="Number of bootstraps", type=int)
    parser.add_argument("-r", help="Number of repetitions", type=int)
    parser.add_argument("-e", help="Number of epochs", type=int)
    parser.add_argument("-v", help="Validation size", type=float)
    parser.add_argument("-s", help="Number of cross-validation splits", type=int)
    parser.add_argument("-c", help="Number of cross-validation repetitions", type=int)
    parser.add_argument("-l", help="Learning rate", type=float)
    parser.add_argument("-b", help="Batch size", type=int)
    parser.add_argument("-d", help="Dropout proportion", type=float)
    parser.add_argument("-j", help="Number of jobs", type=int)
    args = parser.parse_args()
    popfinder_path = args.p
    nboots = args.n
    nreps = args.r
    epochs = args.e 
    valid_size = args.v 
    cv_splits = args.s
    cv_reps = args.c 
    learning_rate = args.l 
    batch_size = args.b
    dropout_prop = args.d
    num_jobs = args.j

    if num_jobs == -1:
        num_jobs = mp.cpu_count()
    pool = mp.Pool(processes=num_jobs)
    results = pool.map(_train_on_bootstraps, [[popfinder_path, nboots, epochs, valid_size, cv_splits,
                                               cv_reps, learning_rate, batch_size,
                                               dropout_prop, rep] for rep in range(nreps)])
    pool.close()
    pool.join()

    test_locs_final = pd.DataFrame()
    pred_locs_final = pd.DataFrame()
    for rep in range(nreps):
        test_locs = results[rep][0]
        pred_locs = results[rep][1]
        test_locs["rep"] = rep
        pred_locs["rep"] = rep
        test_locs_final = pd.concat([test_locs_final, test_locs])
        pred_locs_final = pd.concat([pred_locs_final, pred_locs])

    test_locs_final.to_csv(os.path.join(popfinder_path, "test_locs_final.csv"), index=False)
    pred_locs_final.to_csv(os.path.join(popfinder_path, "pred_locs_final.csv"), index=False)