# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 19:09:01 2021

@author: 
"""

import pandas as pd


# conceptnet words
conceptnet= pd.read_csv('ConceptNet.csv')
conceptnet = conceptnet['Term'].to_list()

cn_words=[]
for word in conceptnet:
    if '_' in word:
        print(word)
        words = word.split('_')
        for w in words:
            cn_words.append(w)
    else:
        cn_words.append(word)

conceptnet = list(set(cn_words))


# onelook positive
onelookpositive = pd.read_csv('outlook527words.csv',encoding='latin-1')
onelookpositive = onelookpositive['Terms'].to_list()

cn_words=[]
for word in onelookpositive:
    words = word.split(' ')
    for w in words:
        cn_words.append(w)

onelookpositive = list(set(cn_words))

all_pos = conceptnet + onelookpositive
all_pos = list(set(all_pos))


# onelook negative for 'apple'
f = open("onelookapple.txt", "r")
onelooknegative= [x for x in f]
onelooknegative= [onelooknegative[i] for i in range(len(onelooknegative)) if i % 2 == 0] 
onelooknegative=  [x.split('.')[1].strip().lower() for x in  onelooknegative]

cn_words=[]
for word in onelooknegative:
    words = word.split(' ')
    for w in words:
        cn_words.append(w)

onelooknegative = list(set(cn_words))

all_neg = onelooknegative

# removing commom elements from both positive and negative lists
def common_member(a, b):     
    a_set = set(a) 
    b_set = set(b) 
      
    # check length  
    if len(a_set.intersection(b_set)) > 0: 
        return(a_set.intersection(b_set))   
    else: 
        return("no common elements")

ff= common_member(all_pos, all_neg)

for ele in ff:
    all_pos.remove(ele)
    all_neg.remove(ele)




# removing elements not in wiki news and twitter gensim corpus
    
import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec
model = api.load("fasttext-wiki-news-subwords-300")

pos_not_in_wiki=[]
for word in all_pos:
    try:
        model.similarity('pedestrian', word)
    except:
        pos_not_in_wiki.append(word)


neg_not_in_wiki=[]
for word in all_neg:
    try:
        model.similarity('pedestrian', word)
    except:
        neg_not_in_wiki.append(word)

# eliminating words
for word in pos_not_in_wiki:
    all_pos.remove(word)

for word in neg_not_in_wiki:
    all_neg.remove(word)


import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec
model1 = api.load("glove-twitter-200")

pos_not_in_twitter=[]
for word in all_pos:
    try:
        model1.similarity('pedestrian', word)
    except:
        pos_not_in_twitter.append(word)


neg_not_in_twitter=[]
for word in all_neg:
    try:
        model1.similarity('pedestrian', word)
    except:
        neg_not_in_twitter.append(word)

# eliminating words
for word in pos_not_in_twitter:
    all_pos.remove(word)

for word in neg_not_in_twitter:
    all_neg.remove(word)




#### making the final dataframe

# final words
full_data = all_pos + all_neg


# creating a dataframe for the pos and negatice data with labels

# creating pos labels
pos_label = [1] * len(all_pos)
# creating neg labels
neg_label = [0] * len(all_neg)

full_labels = pos_label + neg_label

d = {'term': full_data, 'label': full_labels}
df = pd.DataFrame(data=d)
df

wiki_news_sim_score=[]
twitter_sim_score=[]
for w in full_data:
    wiki_news_sim_score.append(model.similarity('pedestrian', w))
    twitter_sim_score.append(model1.similarity('pedestrian', w))


df['wiki_news_sim_score']=wiki_news_sim_score
df['twitter_sim_score']=twitter_sim_score

# savepoint for future use
df.to_csv('partial_data.csv', index=False)



# checking for tweets
import pickle
infile = open('tweets','rb')
all_tweets = pickle.load(infile)
infile.close()

tweet_occ_dict={}
for word in full_data:
    total_occu_count = 0
    for tweet in all_tweets:
        if word in tweet:
            total_occu_count +=1
    tweet_occ_dict[word]=total_occu_count


tweet_yes_no=[]
tweet_count=[]
for word in full_data:
    tweet_count.append(tweet_occ_dict[word])
    if tweet_occ_dict[word] != 0:
        tweet_yes_no.append(1)
    else:
        tweet_yes_no.append(0)


df['tweet_yes_no']=tweet_yes_no
df['tweet_count']=tweet_count

# savepoint for future use
df.to_csv('partial_data.csv', index=False)



# getting wiki data
import pickle
infile = open('listwikiarticleswithped','rb')
pedes_articles = pickle.load(infile)
infile.close()


import pandas as pd
df=pd.read_csv('partial_data.csv')

all_terms = df['term'].to_list()


# term in wikipedia section
import json
list_of_sections=[]
article_no=0
for line in pedes_articles:
    print(article_no)
    article_no+=1
    article = json.loads(line)
    for section_text in article['section_texts']:
        list_of_sections.append(section_text)


dict_word_sections={}
valid_section=[]
word_itr_no=0
for word in all_terms:
    print(word_itr_no)
    word_itr_no+=1

    word_occu=0
    for section_text in list_of_sections:
        if (word in section_text or word.capitalize() in section_text)  and ('pedestrian' in section_text or 'Pedestrian' in section_text):
            word_occu+=1
            valid_section.append(section_text)
    dict_word_sections[word]=word_occu

valid_section = list(set(valid_section))


# term in wikipedia paragraph
import json
list_of_paragraphs=[]
article_no=0
for line in pedes_articles:
    print(article_no)
    article_no+=1
    list_of_list_paragraphs_in_one_article=[]
    article = json.loads(line)
    for section_text in article['section_texts']:
        list_of_list_paragraphs_in_one_article.append(section_text.split('\n'))
    for list_ofparagraphs_in_one_article in list_of_list_paragraphs_in_one_article:
        for one_para in list_ofparagraphs_in_one_article:
            if len(one_para)>3:
                list_of_paragraphs.append(one_para)

dict_word_paragraph={}
valid_paragraph=[]
word_itr_no=0
for word in all_terms:
    print(word_itr_no)
    word_itr_no+=1    
    
    word_occu=0
    for each_paragraph in list_of_paragraphs:
        if (word in each_paragraph or word.capitalize() in each_paragraph) and ('pedestrian' in each_paragraph or 'Pedestrian' in each_paragraph):
            word_occu+=1
            valid_paragraph.append(section_text)
    dict_word_paragraph[word]=word_occu


valid_paragraph = list(set(valid_paragraph))



same_section_count=[]
same_paragraph_count=[]
for word in all_terms:
    same_section_count.append(dict_word_sections[word])
    same_paragraph_count.append(dict_word_paragraph[word])

df['same_section_count']=same_section_count
df['same_paragraph_count']=same_paragraph_count


# savepoint for future use
df.to_csv('partial_data.csv', index=False)

same_sec_yes_no=[]
same_para_yes_no=[]
for word in all_terms:
    if dict_word_sections[word] != 0:
        same_sec_yes_no.append(1)
    else:
        same_sec_yes_no.append(0)

for word in all_terms:
    if dict_word_paragraph[word] != 0:
        same_para_yes_no.append(1)
    else:
        same_para_yes_no.append(0)


df['same_sec_yes_no']=same_sec_yes_no
df['same_para_yes_no']=same_para_yes_no

# savepoint for future use
df.to_csv('partial_data.csv', index=False)


dict_word_article={}  
term_itr_no=0
for term in all_terms:
    print(term_itr_no)
    term_itr_no+=1
    term_count=0
    for line in pedes_articles:
        article = json.loads(line)
        for section_text in article['section_texts']:
            if term in section_text:
                term_count+=1
                break
    dict_word_article[term]=term_count



word_article_count=[]
word_article_yes_no=[]
for word in all_terms:
    if dict_word_article[word] != 0:
        word_article_yes_no.append(1)
    else:
        word_article_yes_no.append(0)

for word in all_terms:
    word_article_count.append(dict_word_article[word])


df['word_article_yes_no']=word_article_yes_no
df['word_article_count']=word_article_count

# savepoint for future use
df.to_csv('partial_data.csv', index=False)














#########
## WORKING ON TEST DATA
#########

# Google books n gram

google_books_words= pd.read_csv('test_googlebooksngram.csv')

google_books_words = google_books_words['Nouns'].to_list()

google_books_words = list(set(google_books_words))


vis_terms= pd.read_csv('test_terms_with_person.csv')

vis_terms = vis_terms['Object'].to_list()

vis_terms = list(set(vis_terms))


# using wikipedia corpus for filtering neg instances
import gensim.downloader as api
model = api.load("glove-wiki-gigaword-100") 



neg_in_wiki=[]
for word in google_books_words:
    try:
        model.similarity('pedestrian', word)
        neg_in_wiki.append(word)
    except:
        continue

after_wiki=[]
for word in neg_in_wiki:
    if model.similarity('pedestrian', word) > 0.3258 :
        after_wiki.append(word)


# using gensim for google news
import gensim
model1 = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

neg_in_google=[]
for word in after_wiki:
    try:
        model1.similarity('pedestrian', word)
        neg_in_google.append(word)
    except:
        continue

after_google=[]
for word in neg_in_google:
    if model1.similarity('pedestrian', word) > 0.2137 :
        after_google.append(word)



all_neg_terms = after_google + vis_terms

all_neg_terms = list(set(all_neg_terms))



final_test_terms = all_neg_terms




import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec
model = api.load("fasttext-wiki-news-subwords-300")


pos_not_in_wiki=[]
for word in final_test_terms:
    try:
        model.similarity('pedestrian', word)
    except:
        pos_not_in_wiki.append(word)


# eliminating words
for word in pos_not_in_wiki:
    final_test_terms.remove(word)


import gensim.downloader as api
# from gensim.models.word2vec import Word2Vec
model1 = api.load("glove-twitter-200")

pos_not_in_twitter=[]
for word in final_test_terms:
    try:
        model1.similarity('pedestrian', word)
    except:
        pos_not_in_twitter.append(word)


# eliminating words
for word in pos_not_in_twitter:
    final_test_terms.remove(word)




# making test dataframe

full_labels = [1] * len(final_test_terms)

d = {'term': final_test_terms, 'label': full_labels}
test_df = pd.DataFrame(data=d)
test_df


wiki_news_sim_score=[]
twitter_sim_score=[]
for w in final_test_terms:
    wiki_news_sim_score.append(model.similarity('pedestrian', w))
    twitter_sim_score.append(model1.similarity('pedestrian', w))

test_df['wiki_news_sim_score']=wiki_news_sim_score
test_df['twitter_sim_score']=twitter_sim_score

# savepoint for future use
test_df.to_csv('test_data.csv', index=False)


# checking for tweets
import pickle
infile = open('tweets','rb')
all_tweets = pickle.load(infile)
infile.close()

tweet_occ_dict={}
for word in final_test_terms:
    total_occu_count = 0
    for tweet in all_tweets:
        if word in tweet:
            total_occu_count +=1
    tweet_occ_dict[word]=total_occu_count


tweet_yes_no=[]
tweet_count=[]
for word in final_test_terms:
    tweet_count.append(tweet_occ_dict[word])
    if tweet_occ_dict[word] != 0:
        tweet_yes_no.append(1)
    else:
        tweet_yes_no.append(0)


test_df['tweet_yes_no']=tweet_yes_no
test_df['tweet_count']=tweet_count

# savepoint for future use
test_df.to_csv('test_data.csv', index=False)





dict_word_sections={}
valid_section=[]
word_itr_no=0
for word in final_test_terms:
    print(word_itr_no)
    word_itr_no+=1

    word_occu=0
    for section_text in list_of_sections:
        if (word in section_text or word.capitalize() in section_text)  and ('pedestrian' in section_text or 'Pedestrian' in section_text):
            word_occu+=1
            valid_section.append(section_text)
    dict_word_sections[word]=word_occu

valid_section = list(set(valid_section))





dict_word_paragraph={}
valid_paragraph=[]
word_itr_no=0
for word in final_test_terms:
    print(word_itr_no)
    word_itr_no+=1    
    
    word_occu=0
    for each_paragraph in list_of_paragraphs:
        if (word in each_paragraph or word.capitalize() in each_paragraph) and ('pedestrian' in each_paragraph or 'Pedestrian' in each_paragraph):
            word_occu+=1
            valid_paragraph.append(section_text)
    dict_word_paragraph[word]=word_occu


valid_paragraph = list(set(valid_paragraph))









same_section_count=[]
same_paragraph_count=[]
for word in final_test_terms:
    same_section_count.append(dict_word_sections[word])
    same_paragraph_count.append(dict_word_paragraph[word])

test_df['same_section_count']=same_section_count
test_df['same_paragraph_count']=same_paragraph_count


# savepoint for future use
test_df.to_csv('test_data.csv', index=False)

same_sec_yes_no=[]
same_para_yes_no=[]
for word in final_test_terms:
    if dict_word_sections[word] != 0:
        same_sec_yes_no.append(1)
    else:
        same_sec_yes_no.append(0)

for word in final_test_terms:
    if dict_word_paragraph[word] != 0:
        same_para_yes_no.append(1)
    else:
        same_para_yes_no.append(0)


test_df['same_sec_yes_no']=same_sec_yes_no
test_df['same_para_yes_no']=same_para_yes_no

# savepoint for future use
test_df.to_csv('test_data.csv', index=False)




dict_word_article={}  
term_itr_no=0
for term in final_test_terms:
    print(term_itr_no)
    term_itr_no+=1
    term_count=0
    for line in pedes_articles:
        article = json.loads(line)
        for section_text in article['section_texts']:
            if term in section_text:
                term_count+=1
                break
    dict_word_article[term]=term_count



word_article_count=[]
word_article_yes_no=[]
for word in final_test_terms:
    if dict_word_article[word] != 0:
        word_article_yes_no.append(1)
    else:
        word_article_yes_no.append(0)

for word in final_test_terms:
    word_article_count.append(dict_word_article[word])


test_df['word_article_yes_no']=word_article_yes_no
test_df['word_article_count']=word_article_count

# savepoint for future use
test_df.to_csv('test_data.csv', index=False)



ml_dataset = pd.concat([df,test_df])

ml_dataset.to_csv('ml_dataset.csv', index=False)


with open('57texualterms.csv', "w") as outfile:
    for entries in after_google:
        outfile.write(entries)
        outfile.write("\n")


import nltk
tagged = nltk.pos_tag(after_google) 

import csv
with open('POS.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['term','POS tag'])
    for row in tagged:
        csv_out.writerow(row)

POScsv = pd.read_csv('POS.csv')
POScsv.to_csv('POS.csv',index=False)



# reading the negative test instances
import pickle
infile = open('apple_terms','rb')
apple_terms = pickle.load(infile)

apple_terms = list(set(apple_terms))












# using wikipedia corpus for filtering neg instances
import gensim.downloader as api
model = api.load("glove-wiki-gigaword-100") 



test_apple_in_wiki=[]
for word in apple_terms:
    try:
        model.similarity('apple', word)
        test_apple_in_wiki.append(word)
    except:
        continue


# using gensim for google news
import gensim
model1 = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)



test_apple_in_google=[]
for word in apple_terms:
    try:
        model1.similarity('apple', word)
        test_apple_in_google.append(word)
    except:
        continue


common_apples= common_member(test_apple_in_google, test_apple_in_wiki)

common_apples=list(set(common_apples))

common_apples.remove('apple')
common_apples.remove('apples')

common_apples = [word.lower() for word in common_apples]




wiki_sim_score_apple_test={}
googlenews_sim_score_apple_test={}

for word in common_apples:
    wiki_sim_score_apple_test[word]=model.similarity('apple', word)
    googlenews_sim_score_apple_test[word]=model1.similarity('apple',word)


import operator
dict1 =sorted(wiki_sim_score_apple_test.items(),key=operator.itemgetter(1),reverse=True)


import operator
dict2 =sorted(googlenews_sim_score_apple_test.items(),key=operator.itemgetter(1),reverse=True)


import pickle
outfile = open('406wikitermsandsimscoresdesc','wb')
pickle.dump(dict1,outfile)
outfile.close()

import pickle
outfile = open('406googlenewstermsandsimscoresdesc','wb')
pickle.dump(dict2,outfile)
outfile.close()

dict1_keys= list(dict1.keys())
dict2_keys =list(dict2.keys())

dict1_keys_half=dict1_keys[0:275]
dict2_keys_half=dict2_keys[0:275]

half_common_apples = common_member(dict1_keys_half,dict2_keys_half)
half_common_apples


import pickle
outfile = open('199negativetestinstances','wb')
pickle.dump(half_common_apples,outfile)
outfile.close()











