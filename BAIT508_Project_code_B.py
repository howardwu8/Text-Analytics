# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 23:16:56 2017

@author: Howard
"""
#Question B.	[Preliminary Analysis; 20 points] Using the collect tweets


import nltk
import string
import json
from collections import Counter

#packages

p = string.punctuation
table_p = str.maketrans(p, len(p) * " ") #punctuation remover
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(["rt", "i'm", "co", "porte", "ton", "ses", "kan", "travail", "mamene", "lorenzo"]) #defining stop words
championtext = ''
sumcount = 0
nostop_wlst = []
withstop_wlst = []
hash_list = []
mention_list = []
usern_list = []
t = ''
#define global variables

def findinfluence(RQT):
    global sumcount
    global championtext
    quotec = RQT['quote_count']
    retweetc = RQT['retweet_count']
    replyc = RQT['reply_count']
    sumc = quotec + retweetc + replyc
    if sumc > sumcount:
        championtext = RQT['text']
        sumcount = sumc
    return championtext
    return sumcount
#define infludence amount function


for runs in range(0,100):
    with open('tweet_stream_Cannabis_100_{}.json'.format(runs), 'r') as g:
        tweets = json.load(g)    

    for item in tweets:

#Question a. What are the ten most popular keywords with and without stop words?

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
            withstop_wlst.append(word)
            if word not in stopwords and len(word) > 1:
                nostop_wlst.append(word) 

#Question b.	What are the ten most popular hashtags (#hashtag)?
        hashtag = item['entities']['hashtags']
        for hash in hashtag:
            hash_list.append(hash['text'].lower())
        
#Question c.	What are the ten most frequently appearing usernames (@username)?            
        mentions = item['entities']['user_mentions']
        for ment in mentions:
            mention_list.append(ment['screen_name'])

#Question d.	Who is the most frequently tweeting person about the keyword?        
        username=item['user']['screen_name']
        usern_list.append(username)   
        
#Question e.	Which is the most influential tweet?         
        if 'retweeted_status' in item:
            i = item['retweeted_status']
            findinfluence(i)
        if 'quoted_status' in item:
            j = item['quoted_status']
            findinfluence(j)
        findinfluence(item)
        
#Result Output:
hashclist = Counter(hash_list).most_common(10)
nonstopc = Counter(nostop_wlst).most_common(10)
print(type(nonstopc))
withstopc = Counter(withstop_wlst).most_common(10)
mentc = Counter(mention_list).most_common(10)
tweetp = Counter(usern_list).most_common(1)

print('Question a: The 10 most popular keywords with stop words are: {}'.format(withstopc))
print('Question a: The 10 most popular keywords without stop words are: {}'.format(nonstopc))
freq = nltk.FreqDist(nostop_wlst)
freq.plot(25)
# plt(freq, interactive = False, key = "0")



print('Question b: The 10 most common Hashtags are: {}'.format(hashclist))
print('Question c: The 10 most frequently appearing usernames are: {}'.format(mentc))
print('Question d: The most frequently tweeting person about the keyword is: {}'.format(list(tweetp[0])[0]))
print('Question e: The most influential tweet is: "{}", with total {} in rt,quotes and replies'.format(championtext, sumcount))


#Code source: UBC BAIT508 Professor Gene Lee