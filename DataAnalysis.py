#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Last updated on :
# Time-stamp: <2023-22-05 16:54:42 arthur.bert@hec.edu>
# PCBS - Prog201 Cogmaster ENS-PSL 2023

# This is the continuation file from ExperimentLetterSize.py.

import pandas
import os

##############################################################################
# V. Data formating, analysis, and saving.
##############################################################################

# Locate data
abspath = os.path.abspath('') # String containing absolute path to the script file
os.chdir(abspath) # Setting up working directory
dataPath = abspath+"/data"
listDir = os.listdir(dataPath)

dataList = []
for item in listDir:
    if item[0:10] == 'Experiment':
        dataList.append(dataPath+"/"+item)

# Extract data
data = []
for dataPath in dataList:
    tempDataframe = pandas.read_csv(dataPath,delimiter=",",
                                     comment='#')
    data.append(tempDataframe)