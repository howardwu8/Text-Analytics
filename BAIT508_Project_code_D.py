# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:11:33 2017

@author: a93163
"""
#Question D: Sentiment Analysis
from os import path
from textblob import TextBlob
import json
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

sub_list = []
pol_list = []
for i in range(0,100):
    with open('tweet_stream_Cannabis_100_{}.json'.format(i), 'r') as g:
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
             tb = '' 
             for ws in text:
                 tb += ws
             tbb = TextBlob(tb)
             sub_list.append(tbb.sentiment.subjectivity)
             pol_list.append(tbb.sentiment.polarity)


n, bins, patches = plt.hist(sub_list, bins=20, facecolor='green',alpha=0.95,)
(mu, sigma) = norm.fit(sub_list)
y = mlab.normpdf( bins, mu, sigma)
#l = plt.plot(bins, y, 'r--', linewidth=2)
#GitHub Code: https://stackoverflow.com/questions/44630658/difference-scipy-stats-norm-mlab-normpdf-and-fitting-gaussian
plt.xlabel('subjectivity score')
plt.ylabel('tweet count')
plt.grid(True)
# reference: https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
plt.savefig(path.join("subjectivity.png"),dpi=600)
plt.show()
print(sum(sub_list)/len(sub_list))



n, bins, patches = plt.hist(pol_list, bins=20, facecolor='green',alpha=0.95,)
(mu, sigma) = norm.fit(pol_list)
y = mlab.normpdf( bins, mu, sigma) 
#l = plt.plot(bins, y, 'r--')
#GitHub Code: https://stackoverflow.com/questions/44630658/difference-scipy-stats-norm-mlab-normpdf-and-fitting-gaussian
plt2 = plt.xlabel('polarity score')
plt2 = plt.ylabel('tweet count')
plt2 = plt.grid(True)
# reference: https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib
plt.savefig(path.join("plolarity.png"),dpi=600)
print(sum(pol_list)/len(pol_list))

#Code Source#1:  UBC BAIT508 Professor Gene Lee;
#Code Source#2:  GitHub Code: https://stackoverflow.com/questions/44630658/difference-scipy-stats-norm-mlab-normpdf-and-fitting-gaussian
#Code Source#3   Stackflow Code: https://stackoverflow.com/questions/9622163/save-plot-to-image-file-instead-of-displaying-it-using-matplotlib