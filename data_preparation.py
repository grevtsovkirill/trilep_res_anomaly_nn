import pandas
import numpy as np


def weight_df(df):    
    df['lumiscale'] = df.RunYear.apply(
               lambda x: (36074.6 if (x == 2015 or x == 2016) else 43813.7))
    weights = df.lumiscale*df.pileupEventWeight_090*df.scale_nom*df.JVT_EventWeight*df.MV2c10_70_EventWeight*df.lepSFObjTight*df.lepSFTrigTight*df.SherpaNJetWeight
    return weights

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


#apply additional selections
def apply_3l_Zveto_SF_cuts(df):
    df1=df.loc[abs(df.lep_ID_0)==abs(df.lep_ID_1)]
    df2=df1.loc[df1.best_Z_Mll>0]    
    return df2


def list_branch_to_remove(df,additional_vars=[]):
    syst_list=['UP','DOWN','CRB','scale','weight','SF','Eff',
               'forFit','HLT','tau','MV2c20','is1','is2','is3','is4',
               'ghost','flvWtOrdr','pass','mc_channel_number','truth',
               'isBrems','isTruth','isQMisID','isExtConv','isConv',
               'isIntConv','isISR','ist','isFake','isLepFromPhEvent',
               'isPrompt','top_','isW','MEphoton','jet_flavor',
               'pileupEventWeight_090','JVT_EventWeight','SherpaNJetWeight','mcWeightOrg','EventWeight',
               'isPrompt','isV','higgs','Clas','bcid','lbn','EventNumber','entry','RunNumber']
    syst_list=syst_list+additional_vars
    matches_syst=[]
    features = list(df.columns.values)
    for x in features:
        for j in syst_list:
            if j in x:
                matches_syst.append(x.strip())
    return matches_syst

def unify_branches(df_1,df_2):
    s1 = set(df_1.columns)
    list_diff12 = [x for x in df_2.columns if x not in s1]
    df_2m = df_2.drop(list_diff12,axis=1)

    s2 = set(df_2m.columns)
    list_diff21 = [x for x in df_1.columns if x not in s2]
    df_1m = df_1.drop(list_diff21,axis=1)
    #df_1m = df_1
        
    #print(list_diff12,list_diff21)
    if set(df_1m.columns)==set(df_2m.columns):
        print("All good, content is the same in both classes\n total %s branches" %len(df_1m.columns))
    else:
        print("WARNING: Something went wrong, double check the content")

    return df_1m,df_2m

def test_nans_float32_infs(df):
    out_boundaries = []
    for i in df.columns:
        val = df[i].sum()
        if float(val)>1e+30:
            print("   --- inf or >float32:",i,val)
            out_boundaries.append(i)
        elif df[i].isnull().any():
            print("   --- contain nans:", i)
            out_boundaries.append(i)
    if out_boundaries:
        df.drop(out_boundaries,axis=1, inplace=True)

    return df

def only_unique(df):
    list_same_val_branch = []
    for j in df.columns:
        i0=df[j].sample(1,random_state=0).item()
        if all(i ==i0 for i in df[j]):
            list_same_val_branch.append(j)

    if list_same_val_branch:
        df.drop(list_same_val_branch,axis=1, inplace=True)

    return df
            
def model_input(df1,df2):
    df1['ltype'] = 1
    df2['ltype'] = 0    
    X = pandas.concat([df1,df2], sort=True)
    y = X['ltype']
    X.drop(['ltype','label','t_w'],axis=1, inplace=True)
    X=test_nans_float32_infs(X)
    X=only_unique(X)
    return X,y


                    
