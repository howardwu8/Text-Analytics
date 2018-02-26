# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 11:38:33 2017

@author: Howard
"""

#Question E: Insights Analysis

from os import path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.manifold import MDS
from scipy.cluster.hierarchy import ward, dendrogram
from sklearn import decomposition
import numpy as np
import nltk
import json
import matplotlib.pyplot as plt
import string
#packages

#variables
p = string.punctuation
table_p = str.maketrans(p, len(p) * " ") #punctuation remover
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["rt", "i'm", "co", "porte", "ton", "ses", "kan", "travail", "mamene", "lorenzo"])
lemma = nltk.wordnet.WordNetLemmatizer()
stemlst = []
nostop_wlst = []
twtname = []
twtall = []
tweetcount = 0
cleandoc = ''

for runs in range(0,100):
    with open('tweet_stream_Cannabis_100_{}.json'.format(runs), 'r') as g:
        tweets = json.load(g)    

    for item in tweets:
        if 'extended_tweet' in item:
            text = item['extended_tweet']['full_text'].lower()
        else:
            text = item['text'].lower()
        t = text.split()
        text = ''
        for s in t:
            if 'http' not in s:
                text += s+' '
        text = text.translate(table_p)
        text = nltk.word_tokenize(text)
        for word in text:
            if word not in stopwords and len(word) > 1:
                cleandoc += word + ' ' 
    twtall.append(cleandoc)
    cleandoc = ''
    tweetcount += 1
    twtname.append('{}-{}'.format(tweetcount*100-99,tweetcount*100))


vectorizer = TfidfVectorizer()
twt_matrix = vectorizer.fit_transform(twtall)


cos_dist = cosine_distances(twt_matrix)
mds = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
pos = mds.fit_transform(cos_dist)
xs, ys = pos[:,0], pos[:,1]

for x, y, name in zip(xs, ys, twtname):
    plt.scatter(x, y)
    plt.text(x, y, name)
    
plt.title('tweet MDS')
plt.savefig(path.join("factor_analysis.png"),dpi=600)
plt.show()

linkage_matrix = ward(cos_dist)
dendrogram(linkage_matrix, orientation='left', labels=twtname)
plt1= plt.tight_layout()
# reference: https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
plt.savefig(path.join("dendrogram.png"),dpi=600)
plt1=plt.show()

#threshold = 0.5
#sim_list = []
#for doc1 in twtall:
#    for doc2 in twtall:
#        if doc1 <= doc2:
#            continue
#        sim = SequenceMatcher(None, doc1, doc2).ratio()
#        sim_list.append(sim)
#        if sim > threshold:
#            print(doc1)
#            print(doc2)
       
#print(np.mean(sim_list), np.std(sim_list))
#print(max(sim_list))

#plt2=plt.hist(sim_list, bins=20) #, normed=1, alpha=0.75)
#plt2=plt.xlabel('similarity score')
#plt2=plt.ylabel('pair count')
#plt2=plt.grid(True)
#plt.savefig(path.join("hist.png"),dpi=1200)
#plt2=plt.show()

#print(type(twt_matrix))
#print(twt_matrix)

# This code takes too much running time as it will be running 100 power of 100 times, 
# and we don't really get too much insight from it. The similarity score is not very intuitive on our topic.


vocab = vectorizer.get_feature_names() # list of unique vocab, we will use this later
print(len(vocab)) #, '# of unique words'
print(vocab[-10:])
print(vocab[:10])
print(twt_matrix.shape)


num_topic = 3
# initialize the NMF decomposition with 10 components (topics)
clf = decomposition.NMF(n_components = num_topic, random_state=1)
# fit the NMF model with document-term TF-IDF matrix
doctopic = clf.fit_transform(twt_matrix)
# check the error
print(num_topic, clf.reconstruction_err_)
topic_words = []
num_top_words = 30

for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][:num_top_words]
    for idx in word_idx:
        print(vocab[idx], end= ' ')
    topic_words.append([vocab[i] for i in word_idx])
    print('\n')

#Code Source#1:  UBC BAIT508 Professor Gene Lee;
#Code Source#2:  https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib