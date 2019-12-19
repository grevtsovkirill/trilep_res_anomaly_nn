# Anomaly investigation

## Introduction
Trilepton selection has particular 2b region where invariant mass of the same flavour lepton pair creates a peak.
The conventional methods to investigate the origin have been resultless. The idea is to build NN model using all possible properties as an input features, and rank which of them point to the highest separation between two classes in the peak region.


## Files
To compare distributions, internal code used to produce ```root``` format files have been produced.
In order to be able to use spark or other types of dataframe compatible to pythin, convertor was created.
It can be found in ```Files/convertor.py```, all possible options are listen in  ```-h```.
An example to run:
```
python3 convertor.py -f class_mc_TYPE -i /local/Files -o /local/myOutPath -t nominal -d csv
```

