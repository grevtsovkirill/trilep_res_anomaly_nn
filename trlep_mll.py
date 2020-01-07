
import sys,os,time,stat,logging
import pandas
import numpy as np
import data_preparation
import plot_helper

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def weight_df(df):    
    df['lumiscale'] = df.RunYear.apply(
               lambda x: (36074.6 if (x == 2015 or x == 2016) else 43813.7))
    weights = df.lumiscale*df.pileupEventWeight_090*df.scale_nom*df.JVT_EventWeight*df.MV2c10_70_EventWeight*df.lepSFObjTight*df.lepSFTrigTight*df.SherpaNJetWeight
    return weights

#load MC samples:
def data_load():
    df=pandas.read_csv('Files/class_data.csv')
    df['t_w'] = 1
    df['label'] = 'data'    
    return df
    
def mc_load(labels_list):
    mc_list=[]
    for i in labels_list:
        name='Files/class_mc_'+i+'.csv'
        df=pandas.read_csv(name)
        df['label'] = i
        if i == 'fakes':
            df['t_w'] = 1
        else:
            df['t_w'] = weight_df(df)
        
        mc_list.append(df)
        
    mc_df = pandas.concat(mc_list,sort=False)
    return mc_df

def get_data(labels_list):
    data = data_load()
    bkg = mc_load(labels_list)
    return data,bkg
    


def main():
    #load data 
    #labels_list=['ttZ','ttW','ttH','VV','fakes','Others']
    labels_list=['ttZ']
    data, bkg_set=get_data(labels_list)

    #apply final selections
    data_sel=data_preparation.apply_3l_Zveto_SF_cuts(data)
    bkg_set_sel=data_preparation.apply_3l_Zveto_SF_cuts(bkg_set)
    
    var='Mll01'
    #test stack plot of whole contributions 
    plot_helper.plot_stack_var(data_sel,bkg_set_sel,labels_list,'Mll01',0.001)

    #plot of two classes to find the key feature responsible for the difference
    plot_helper.ovr_slot(data_sel,bkg_set_sel)
    
    #prepare datasets for building the model:
    data_sel_trim = data_sel.drop(data_preparation.list_branch_to_remove(data_sel),axis=1)
    bkg_set_sel_trim = bkg_set_sel.drop(data_preparation.list_branch_to_remove(bkg_set_sel),axis=1)

    #check that both classes contains same information: number and type of branches
    data_class,bkg_class = data_preparation.unify_branches(data_sel_trim,bkg_set_sel_trim)

    #build data for the model:
    X,y=data_preparation.model_input(data_class,bkg_class)
    print(len(X.columns))
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

