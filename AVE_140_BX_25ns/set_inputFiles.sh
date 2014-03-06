#!/bin/bash

# Each time the script is invoked on the remote WN, it will be passed
# the proper Job Index, here captured as $1, i.e., we will basically
# process only N-th file among the ones listed on the input list
# file. For this reason we must guarante that the splitting parameters
# contained the the crab config file for this step are **identical**
# to the ones used to generate the signal sample.

filename=$(cat TTbar_fullList.txt | sed -n $1,$1p)
echo "Using $filename as input"
python set_inputFiles.py $filename
mv pset{2,}.py.pkl
cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml -p pset.py
