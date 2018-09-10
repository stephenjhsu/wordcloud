"""
Script to create word cloud stencils from Twitter data

Stephen Hsu
"""

import numpy as np
import matplotlib.pyplot as plt
import re
from twython import Twython
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from IPython.display import Image as im

#Gain access to Twitter data using Twython
APP_KEY = "Dgh9WnBxXeLUcBYhXeohlnazm" #YOUR APP KEY HERE
APP_SECRET = "6fTM5hlYVbMGwVWololl7smrE3BexV6x8EXj7Ye6EJgw2LGA3" #YOUR APP SECRET HERE
twitter = Twython(APP_KEY, APP_SECRET)

def clean_tweets(raw_list):
	"""
	Function to create a string without special characters and 
	URL links. 
	Input:
		raw_list (list): tweet in JSON format
	Output:
		no_special_characters (str): string of cleaned tweets 
	"""
	raw_string = ''.join(raw_tweets)
	no_links = re.sub(r'http\S+', '', raw_string)
	no_unicode = re.sub(r"\\[a-z][a-z]?[0-9]+", '', no_links)
	no_special_characters = re.sub('[^A-Za-z ]+', '', no_unicode)
	return no_special_characters

def create_words(clean_string):
	"""
	Function to create a list of lower case, non-stop words 
	longer than 2 characters/
	Input:
		clean_string (str): string of cleaned text
	Output:
		words (list): list of lowercased, non-stop words 
	"""
	words = clean_string.split(" ")
	words = [w for w in words if len(w) > 2]  # ignore a, to, at...
	words = [w.lower() for w in words]
	return words

#Collect the data from the user timeline
user_timeline = twitter.get_user_timeline(screen_name='',
										count=200, include_rts=False)
raw_tweets = []
for tweets in user_timeline:
    raw_tweets.append(tweets['text'])

#Generate the cloud
clean_text = clean_tweets(raw_tweets)
words = create_words(clean_text)
clean_string = ','.join(words)
mask = np.array(Image.open('/Users/shsu/Downloads/nike.png'))
wc = WordCloud(background_color="white", max_words=2000, mask=mask)
wc.generate(clean_string)

#Visualize the data
f = plt.figure(figsize=(50,50))
f.add_subplot(1,2, 1)
plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.title('Original Stencil', size=40)
plt.axis("off")

f.add_subplot(1,2, 2)
plt.imshow(wc, interpolation='bilinear')
plt.title('Twitter Generated Cloud', size=40)
plt.axis("off")
plt.show(block=True)

