
import sys,os,time,stat,logging
import pandas
import matplotlib.pyplot as plt
import numpy as np
import data_preparation

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

scale_to_GeV=0.001
binning = {
    "DRll01": np.linspace(-2, 6, 24),
    "max_eta": np.linspace(0, 2.5, 26),
    "Mll01": np.linspace(0, 200, 25)
}

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

def plot_stack_var(df_data,df_bkg,lab_list,var,GeV):
    stack_var=[]
    stack_var_w=[]
    stack_var_leg=[]    

    for i in lab_list:
        stack_var.append(df_bkg[var].loc[df_bkg.label==i]*GeV)
        stack_var_w.append(df_bkg.t_w.loc[df_bkg.label==i])
        stack_var_leg.append(i)

    plt.hist( stack_var, binning[var], histtype='step',
         weights=stack_var_w,
         label=stack_var_leg,
         stacked=True, 
         fill=True, 
         linewidth=2, alpha=0.8)
    plt.hist(df_data[var]*GeV, binning[var], histtype='step',
         label=["data"],
         stacked=False, 
         fill=False, 
         color='k',
         linewidth=2, alpha=0.8)
    plt.xlabel(var,fontsize=12)
    plt.ylabel('# Events',fontsize=12) 
    plt.legend()
    plt.tight_layout()
    plt.savefig("Plots/"+var+".png", transparent=True)

def ovr_slot(df_d,df_b,var='Mll01',GeV=0.001,fig_size=(10, 5)):
    f, ax = plt.subplots(figsize=fig_size)
    ax.hist(df_d[var]*GeV, binning[var], histtype='step',
         label=["data"],
         stacked=False, 
         fill=False, 
         linewidth=2, alpha=0.8)
    ax.hist(df_b[var]*GeV, binning[var], histtype='step',
         label=["bkgs"],
         weights=df_b.t_w,
         stacked=False, 
         fill=False, 
         linewidth=2, alpha=0.8)
    ax.set_xlabel(var,fontsize=12)
    ax.set_ylabel('# Events',fontsize=12)    
    ax.legend()   
    f.savefig("Plots/class_"+var+".png", transparent=True)

    


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
    plot_stack_var(data_sel,bkg_set_sel,labels_list,'Mll01',0.001)

    #plot of two classes to find the key feature responsible for the difference
    ovr_slot(data_sel,bkg_set_sel)
    
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

