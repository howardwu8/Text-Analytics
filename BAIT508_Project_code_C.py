# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:13:16 2017

@author: a93163
"""
#Question C Word Cloud

from os import path
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import nltk
import json
import string
from collections import Counter 
#packages


# new and recommended 
# https://stackoverflow.com/questions/24647400/what-is-the-best-stemming-method-in-python
# new approach of stemming
lemma = nltk.wordnet.WordNetLemmatizer()

#punctuation
p = string.punctuation
nostop_wlst = []
withstop_wlst = []
stemlst = []
cloudtext1=''
table_p = str.maketrans(p, len(p) * " ")
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["rt", "i'm", "co"])
# Read the whole text.
for i in range(0,100):
    with open('tweet_stream_Cannabis_100_{}.json'.format(i), 'r') as g:
         tweets = json.load(g)
         for item in tweets:
             if 'extended_tweet' in item:
                 text = item['extended_tweet']['full_text']
             else:
                 text = item['text']
             t = text.split()
             text = ''
             for s in t:
                 if 'http' not in s:
                     text += s+' '
             text = text.translate(table_p)
             text = nltk.word_tokenize(text)   
             for word in text:
                 if word not in stopwords and len(word) > 1:
                     nostop_wlst.append(word)  

for word in nostop_wlst:
    stemlst.append(lemma.lemmatize(word))
st = list(Counter(stemlst).most_common(1000))
for word in st:
    cloudtext1 += ' {}'.format(word[0])

# Generate a word cloud image

# reference: how to use background image and generate color from it when executing a wordcloud: 
#https://amueller.github.io/word_cloud/auto_examples/colored.html
#colored-py

backgroud_Image=plt.imread('cannabis_leaf.jpg') 
wc=WordCloud( 
background_color='white', 
mask=backgroud_Image, 
max_words=500,
max_font_size=40, 
width=1000,
height=1000,
random_state=42
) 
wc.generate_from_text(cloudtext1)  
img_colors=ImageColorGenerator(backgroud_Image) 
wc.recolor(color_func=img_colors) 
plt.imshow(wc) 
plt.axis('off') 
plt.show() 
# reference: method to save wordcloud to local directory 'http://blog.csdn.net/tanzuozhev/article/details/50789226'
wc.to_file(path.join("cloud.png")) #To save the wordcloud into a .png file


#Code Source#1:  UBC BAIT508 Professor Gene Lee;
#Code Source#2:  https://amueller.github.io/word_cloud/auto_examples/colored.html
#Code Source#3:  https://stackoverflow.com/questions/24647400/what-is-the-best-stemming-method-in-python
#Code Source#4:  http://blog.csdn.net/tanzuozhev/article/details/50789226