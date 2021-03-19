# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:38:42 2021

@author: 
"""

import pandas as pd

conceptnet= pd.read_csv('ConceptNet.csv')

outlookpositive = pd.read_csv('outlook527words.csv',encoding='latin-1')


f = open("onelookapple.txt", "r")
outlooknegative= [x for x in f]
outlooknegative22= [outlooknegative[i] for i in range(len(outlooknegative)) if i % 2 == 0] 
outlooknegative22new=  [x.split('.')[1].strip().lower() for x in  outlooknegative22]
outlooknegative= outlooknegative22new
outlooknegative = list(set(outlooknegative))


conceptnet_words = conceptnet['Term'].to_list()
outlookpositive = outlookpositive['Terms'].to_list()






import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec

model = api.load("fasttext-wiki-news-subwords-300")
model.most_similar("pedestrian")


model.similarity('pedestrian', 'crossing')

cn_words=[]
for word in conceptnet_words:
    if '_' in word:
        word  = word.replace('_','-')
        cn_words.append(word)
    else:
        cn_words.append(word)

olpos_words=[]
for word in outlookpositive:
    if ' ' in word:
        word  = word.replace(' ','-')
        olpos_words.append(word)
    else:
        olpos_words.append(word)


olneg_words=[]
for word in outlooknegative:
    if ' ' in word:
        word  = word.replace(' ','-')
        olneg_words.append(word)
    else:
        olneg_words.append(word)


final = cn_words + olpos_words + olneg_words
final_filtered = list(set(final))


cnt=0
valid_wiki=[]
for word in final_filtered:
    try:
        model.similarity('pedestrian', word)
        valid_wiki.append(word)
    except:
        cnt+=1















import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec

model1 = api.load("glove-twitter-200")
model1.most_similar("pedestrian")

cnt_tw=0
valid_twitter=[]
for word in final_filtered:
    try:
        model1.similarity('pedestrian', word)
        valid_twitter.append(word)
    except:
        cnt_tw+=1













# Python program to find common elements in 
# both sets using intersection function in 
# sets 
  
  
# function  
def common_member(a, b):     
    a_set = set(a) 
    b_set = set(b) 
      
    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return("no common elements")


ff= common_member(valid_twitter, valid_wiki)



new_new=[]
for word in final_filtered:
    if '-' in word:
        aa=word.split('-')
        for p in aa:
            new_new.append(p)
    else:
        new_new.append(word)

new_new_no_dups = list(set(new_new))


cnt=0
valid_wiki=[]
for word in new_new_no_dups:
    try:
        model.similarity('pedestrian', word)
        valid_wiki.append(word)
    except:
        cnt+=1



cnt_tw=0
valid_twitter=[]
for word in new_new_no_dups:
    try:
        model1.similarity('pedestrian', word)
        valid_twitter.append(word)
    except:
        cnt_tw+=1