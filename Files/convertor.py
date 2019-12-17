#!/usr/bin/python3

import sys,os,time,stat,logging
import uproot, pandas
from optparse import OptionParser

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


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

    (options, args)=parser.parse_args()
    inpfile = options.inpFile
    inppath = options.inpPath
    outpath = options.outPath
    
    # Check that the input path exists
    if not os.path.exists(inppath):
        log.error("The input path specified doesn't exists.\n\t\t\tPlease, use '-i <path>' to specify an existing input path.")
        sys.exit()
        
    if not os.path.isfile(inppath+"/"+inpfile):
        log.error("The input file specified doesn't exists in the input path.\n\t\t\tPlease, use '-f <file>' to specify an existing file in the path.")
        sys.exit()
        
    if not os.path.exists(outpath):
        log.error("\tThe output path specified doesn't exists.\n\t\t\tPlease, use '-o <path>' to specify an existing output path.")
        sys.exit()
        
    # load input data
    in_data = uproot.open(inppath+"/"+inpfile)["nominal"]
    #in_data_df = in_data.pandas.df()
        

# Start the main routine and log process time
if __name__ == "__main__":
    start = time.time()
    main()
    log.info("]\tProcess time: %f" %(time.time() - start))

        
