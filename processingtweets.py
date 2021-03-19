# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 21:04:37 2021

@author:
"""

import os
import pandas as pd

main_folder = os.getcwd()

all_folders = os.listdir()


all_tweets=[]
for sub in all_folders:
    temp_folder = main_folder
    temp_folder += '\\'
    temp_folder += sub
    os.chdir(temp_folder)
    all_files = os.listdir()
    for file in all_files:
        if file.endswith('csv'):
            sample = pd.read_csv(file)
            all_tweets.extend(sample['text'].to_list())
    os.chdir(main_folder)


import pickle
filename = 'tweets'
outfile = open(filename,'wb')
pickle.dump(all_tweets,outfile)
outfile.close()