#!/usr/bin/python3

import sys,os,time,stat,logging
import uproot, pandas
import numpy as np 
from optparse import OptionParser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def find_vector_branches(in_df):
    vector_branches_list=[]
    #x = np.array(in_df.keys()) 
    #for i in np.unique(x):
    for i in in_df.keys():
        #for j in range(len(in_df[i])):
        for j in range(5):
            if in_df[i][j].size != 1:
                vector_branches_list.append(i)
                break

    return vector_branches_list
    

def main():
    
    parser=OptionParser("python %prog [options]")
    
    parser.add_option("-f", "--inpFile",
		      dest="inpFile",
		      help="Input .root file. Must be specified.")
    parser.add_option("-i", "--inpPath",
		      dest="inpPath",
		      default="./",
		      help="Path where the .root files are stored. Must be specified. [Default = ./].")
    parser.add_option("-o", "--outPath",
		      dest="outPath",
		      default="./",
		      help="Path where the output file will be saved. [Default = ./].")
    parser.add_option("-t", "--inpFileTree",
		      dest="inpFileTree",
		      default="nominal",
		      help="Tree name. [Default = nominal].")
    parser.add_option("-d", "--outFormat",
		      dest="outFormat",
		      default="csv",
		      help="Output format. [Default = csv].")

    (options, args)=parser.parse_args()
    inpfile = options.inpFile
    inpfiletree = options.inpFileTree
    inppath = options.inpPath
    outpath = options.outPath
    format_choice = options.outFormat
    
    # Check that the input path exists
    if not os.path.exists(inppath):
        log.error("The input path specified doesn't exists.\n\t\t\tPlease, use '-i <path>' to specify an existing input path.")
        sys.exit()
        
    if not os.path.isfile(inppath+"/"+inpfile+".root"):
        log.error("The input file specified doesn't exists in the input path.\n\t\t\tPlease, use '-f <file>' to specify an existing file in the path.")
        sys.exit()
        
    if not os.path.exists(outpath):
        log.error("The output path specified doesn't exists.\n\t\t\tPlease, use '-o <path>' to specify an existing output path.")
        sys.exit()
        
    outname=outpath+'/'+inpfile+'.'+format_choice 
    # load input data
    in_data = uproot.open(inppath+"/"+inpfile+".root")[inpfiletree]
    
    in_data_df = in_data.pandas.df(flatten=False)
    #del in_data_df['lep_truthParentPdgId_2_new']
    vector_br_list=find_vector_branches(in_data_df)
    #vector_list=['jet_flavor_truth_label_ghost','jet_flavor_weight_MV2c10','jet_pT','jet_eta','lepton_PromptLeptonIso_TagWeight','lepton_ChargeIDBDTTight','scale_weights','mcEventWeights','total_weights','electron_ambiguityType','electron_PromptLeptonIso_TagWeight','electron_PromptLeptonVeto_TagWeight','muon_PromptLeptonIso_TagWeight','muon_PromptLeptonVeto_TagWeight']
    #print(np.array_equal(vector_br_list,vector_list))
    for i in vector_br_list:
        del in_data_df[i]


    if format_choice == 'csv':
        in_data_df.to_csv(outname, sep=',')        
    elif format_choice == 'h5':
        in_data_df.to_hdf(outname, key='df', mode='w')
    else:
        log.error("Specify format")
        sys.exit()
        
    

# Start the main routine and log process time
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("]\tProcess time: %f" %(time.time() - start))

        
