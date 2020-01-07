import matplotlib.pyplot as plt
import numpy as np
import pandas 
scale_to_GeV=0.001
binning = {
    "DRll01": np.linspace(-2, 6, 24),
    "max_eta": np.linspace(0, 2.5, 26),
    "Mll01": np.linspace(0, 200, 25)
}


def plot_stack_var(df_data,df_bkg,lab_list,var,GeV=scale_to_GeV):
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

def ovr_slot(df_d,df_b,var='Mll01',GeV=scale_to_GeV,fig_size=(10, 5)):
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

def feature_rank(model,df,top_vars=20):
    tree_importance_sorted_idx = np.flip(np.argsort(model.feature_importances_))
    tree_indices = np.arange(0, len(model.feature_importances_)) + 0.5

    f, ax = plt.subplots(figsize=(12, 8))
    ax.barh(tree_indices,
            model.feature_importances_[tree_importance_sorted_idx], height=0.7)
    ax.set_yticklabels(df.columns[tree_importance_sorted_idx])
    ax.set_yticks(tree_indices)
    ax.set_ylim((0,top_vars))
    f.tight_layout()
    f.savefig("Plots/rank20RF.png", transparent=True)

    rank = pandas.DataFrame(list(zip(df.columns[tree_importance_sorted_idx][:top_vars],
                               model.feature_importances_[tree_importance_sorted_idx][:top_vars])),
                      columns =['var', 'score'])
    rank.to_csv('Plots/rank20R.csv')
