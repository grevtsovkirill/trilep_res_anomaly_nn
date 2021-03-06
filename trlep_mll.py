import sys,os,time,stat,logging
import pandas
import numpy as np
import data_preparation
import plot_helper
import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)



def get_data(labels_list):
    data = data_preparation.data_load()
    bkg = data_preparation.mc_load(labels_list)
    return data,bkg
    


def main():
    #load data 
    labels_list=['ttZ','ttW','ttH','VV','fakes','Others']
    #labels_list=['ttZ']
    data, bkg_set=get_data(labels_list)

    #apply final selections
    data_sel=data_preparation.apply_3l_Zveto_SF_cuts(data)
    bkg_set_sel=data_preparation.apply_3l_Zveto_SF_cuts(bkg_set)
    
    var='Mll01'
    #test stack plot of whole contributions 
    plot_helper.plot_stack_var(data_sel,bkg_set_sel,labels_list,var)

    #plot of two classes to find the key feature responsible for the difference
    plot_helper.ovr_slot(data_sel,bkg_set_sel,var)
    
    #prepare datasets for building the model:
    data_sel_trim = data_sel.drop(data_preparation.list_branch_to_remove(data_sel),axis=1)
    bkg_set_sel_trim = bkg_set_sel.drop(data_preparation.list_branch_to_remove(bkg_set_sel),axis=1)

    #check that both classes contains same information: number and type of branches
    data_class,bkg_class = data_preparation.unify_branches(data_sel_trim,bkg_set_sel_trim)

    #build data for the model:
    X,y=data_preparation.model_input(data_class,bkg_class)
    print(len(X.columns))
    '''
    intentionaly keep all data (without split to train and test)
    as the goal to spot key feature in experimental data (label=0)
    leading to issue with the reconstruction process
    '''
    
    #Set of Models
    names = ["DecisionTree", "RandomForest", "AdaBoost"]
    classifiers = [
        DecisionTreeClassifier(max_depth=5),
        RandomForestClassifier(max_depth=5, n_estimators=100),
        AdaBoostClassifier()]

    
    Xs = StandardScaler().fit_transform(X)
    # iterate over classifiers
    for name, clf in zip(names, classifiers):
        clf.fit(X, y)
        plot_helper.feature_rank(clf,X,name)

    

    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

