# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:59:22 2021

@author: 
"""
# saving all the jsons format articles(that have word pedestrian) in a list
ped_data=[]

from gensim import utils
import json
# iterate over the plain text data we just created
with utils.open('enwiki-latest.json.gz', 'rb') as f:
    for line in f:
        # decode each JSON line into a Python dictionary object
        article = json.loads(line)
        # each article has a "title", a mapping of interlinks and a list of "section_titles" and
        # "section_texts".
        
        
        #print("Article title:",article['title'])
        #print("Interlinks:",article['interlinks'])
        for section_title, section_text in zip(article['section_titles'], article['section_texts']):
            #print("Section title:",section_title)
            #print("Section text:",section_text)
            if 'Pedestrian' in section_title or 'pedestrian' in section_title or 'Pedestrian' in section_text or 'pedestrian' in section_text:
                ped_data.append(line)
                break

len(ped_data)

import pickle
filename = 'listwikiarticleswithped'
outfile = open(filename,'wb')
pickle.dump(ped_data,outfile)
outfile.close()
