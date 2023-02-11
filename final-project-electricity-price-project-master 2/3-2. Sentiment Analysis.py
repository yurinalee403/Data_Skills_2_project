
"""
pip install spacytextblob
python -m textblob.download_corpora
from spacytextblob.spacytextblob import SpacyTextBlob
import spacy
import os
import pandas as pd
import requests

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 2000000
nlp.add_pipe('spacytextblob')


ns = pd.read_excel('result_news.xlsx').dropna(axis=1)
link = ns['link']


#get values
news_pol = []
for x in range(len(link)):
    response = requests.get(link[x])
    content = response.text
    doc = nlp(content)
    val = round(doc._.blob.polarity, 4)
    news_pol.append(val)
    x += 1

print(news_pol)


news_sub = []
for x in range(len(link)):
    response = requests.get(link[x])
    content = response.text
    doc = nlp(content)
    val = round(doc._.blob.subjectivity, 4)
    news_sub.append(val)
    x += 1

print(news_sub)




#create a dataframe for plotting
ns['datetime'] = pd.to_datetime(ns['date'])
ns['Polarity'] = news_pol
ns['Subjectivity'] = news_sub
df = ns[['datetime', 'Polarity', 'Subjectivity']]
df = df.sort_values('datetime', ascending=True)


#Sentiment Analysis plotting
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


figure(figsize=(10, 8), dpi=80)
plt.plot(df['datetime'], df['Polarity'], 
        linewidth = 1.5,
        color = 'orange', marker = 'o')
plt.plot(df['datetime'], df['Subjectivity'], 
        linewidth = 1.5,
        color = 'green', marker = 'o')
plt.title('Sentiment Analysis')
plt.ylabel('Value')
plt.xlabel('Dates')

plt.gca().legend(('Polarity','Subjectivity'))

plt.savefig('sentiment_plot.png') 




#Summary Statistics
import statistics

pol_mean = statistics.mean(news_pol)
pol_mean

sub_mean = statistics.mean(news_sub)
sub_mean
