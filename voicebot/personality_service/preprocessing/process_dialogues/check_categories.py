### This file contains code to count the number of combinations
### of sentiment and emotion in the MELD Dataset.

import pandas as pd

df_train = pd.read_csv('./MELD_combined.csv') 
emotions = df_train['Emotion'].tolist() 
sentiments = df_train['Sentiment'].tolist()

categories=[]
for e, s in zip(emotions, sentiments):
    if [e,s] not in categories:
        categories.append([e,s])

print(categories)