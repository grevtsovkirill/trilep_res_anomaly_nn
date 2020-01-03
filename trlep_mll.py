
import sys,os,time,stat,logging
import pandas
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

#load MC samples:
def mc_load(labels_list):
    mc_list=[]
    for i in labels_list:
        name='Files/class_mc_'+i+'.csv'
        df=pandas.read_csv(name)
        df['label'] = i
        if i == 'fakes':
            df['t_w'] = 1
        #else:
        #    df['t_w'] = weight_df(df)
        
        mc_list.append(df)
        
    mc_df = pandas.concat(mc_list,sort=False)
    return mc_df

def main():
    #labels_list=['ttZ','ttW','ttH','VV','fakes','Others']
    labels_list=['ttZ']
    bkg_set=mc_load(labels_list)
    
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("Process time: %f" %(time.time() - start))

