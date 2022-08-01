import pandas as pd


df_train = pd.read_csv('/home/dodev/ben_msc_project/do-voice-interaction/voicebot/personality_service/preprocessing/MELD_combined.csv') 
emotions = df_train['Emotion'].tolist() 
sentiments = df_train['Sentiment'].tolist()

categories=[]
for e, s in zip(emotions, sentiments):
    if [e,s] not in categories:
        categories.append([e,s])

print(categories)