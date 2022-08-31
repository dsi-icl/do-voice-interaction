import pandas as pd
import nlpaug.augmenter.word as naw
from googletrans import Translator



df_train = pd.read_csv('./MELD_combined.csv') 
utt = df_train['Utterance'].tolist() 
sea_id = df_train['Season'].tolist()
epi_id = df_train['Episode'].tolist()
dia_id = df_train['Dialogue_ID'].tolist() 
utt_id = df_train['Utterance_ID'].tolist() 
emotions = df_train['Emotion'].tolist() 
sentiments = df_train['Sentiment'].tolist()
sets = df_train['Set'].tolist()
speakers = df_train['Speaker'].tolist()
stories = []
line_ones = []
line_twos= []

for i in range(len(utt)):
    utt[i]=utt[i].replace('"', '').replace("’", "'")

dia_num=0
dialogues=[]
dialogue=[]
for u, sd, ed, dd, ud, set, emo, sent, spea in zip(utt, sea_id, epi_id, dia_id, utt_id, sets, emotions, sentiments, speakers):
    if (dd==dia_num):
        dialogue.append([set, sd, ed, dd, ud, u, emo, sent, spea])
    else:
        dialogues.append(dialogue)
        dialogue=[]
        dialogue.append([set, sd, ed, dd, ud, u, emo, sent, spea])
        dia_num=dd
dialogues.append(dialogue)

personality = "Phoebe"


if personality=='full':
    for d in dialogues:
        count = 0
        for u in d:
            line_ones.append(u)
            line_twos.append(u)
            count+=1
        line_ones.pop(len(line_ones)-1)
        line_twos.pop(len(line_twos)-count)
else:
    for i in range(len(dialogues)):
        for u in range(1, len(dialogues[i])):
            if dialogues[i][u][8]==personality and dialogues[i][u-1][8]!=personality:
                line_ones.append(dialogues[i][u-1])
                line_twos.append(dialogues[i][u])
    with open(personality+".txt","w") as f:
        for a, b in zip(line_ones, line_twos):
            f.write(str(a)+"\n")
            f.write(str(b)+"\n\n")

responses=[]
intents=[]

for i in range(len(line_ones)):
    stories.append("Dataset:" + line_ones[i][0] + "_Season:" + str(line_ones[i][1]) + "_Episode:" + str(line_ones[i][2]) + "_Dialogue:" + str(line_ones[i][3]) + "_Utterance:" + str(line_ones[i][4])) 
    intents.append([line_twos[i][0] + "_" + str(line_twos[i][1]) + "_" + str(line_twos[i][2]) + "_" + str(line_twos[i][3]) + "_" + str(line_twos[i][4])+","+line_twos[i][6]+","+line_twos[i][7], line_ones[i][5]])
    responses.append([line_twos[i][0] + "_" + str(line_twos[i][1]) + "_" + str(line_twos[i][2]) + "_" + str(line_twos[i][3]) + "_" + str(line_twos[i][4])+","+line_twos[i][6]+","+line_twos[i][7], line_twos[i][5]]) 

aug1 = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="insert", aug_max=4)
aug2 = naw.ContextualWordEmbsAug(model_path='bert-base-uncased', action="substitute", aug_max=4)
translator = Translator()

# YML

with open("./"+personality+"_yml/nlu.yml", "w") as f:
    f.write('version: "3.1"\n')
    f.write("nlu:\n")
    li_no=0
    for identifier, content in intents:
        f.write("- intent: "+"chitchat/"+identifier+"\n")
        f.write("  examples: |\n")
        f.write("    - "+content+"\n")
        f.write("    - "+aug1.augment(content)[0]+"\n")
        f.write("    - "+aug2.augment(content)[0]+"\n")
        f.write("    - "+translator.translate(translator.translate(content, dest='af', src='en').text, dest='en', src='af').text+"\n")
        li_no+=1
        print(li_no)


f.close()

# with open("./"+personality+"_yml/", "w") as f:
#     f.write('version: "3.1"\n')
#     f.write("rules:\n")
#     for s, i, r in zip(stories, intents, responses):
#         f.write("- rule: "+s+"\n")
#         f.write("  steps:\n")
#         f.write("  - intent: "+i[0]+"\n")
#         f.write("  - action: "+r[0]+"\n")
# f.close()

with open("./"+personality+"_yml/domain.yml", "w") as f:
    f.write('version: "3.1"\n\n')
    # f.write("intents:\n")
    # for i in intents:
    #     f.write("  - "+i[0]+"\n")
    f.write("\n\nresponses:\n")
    for r in responses:
        f.write("  "+"utter_chitchat/"+r[0]+":\n")
        f.write('  - text: "'+r[1]+'"\n')
f.close()




# MARKDOWN

# with open("data_md/nlu.md", "w") as f:
#     for u, i in zip(utt, intents):
#         f.write("## intent:"+i+"\n")
#         f.write("- "+u+"\n\n")
# f.close()

# with open("data_md/stories.md", "w") as f:
#     for s, i, r in zip(stories, intents, responseIDS):
#         f.write("## "+s+"\n")
#         f.write("* "+i+"\n")
#         f.write(" - "+r+"\n\n")
# f.close()

# with open("data_md/responseIDS.md", "w") as f:
#     for r, ri in zip(res, responseIDS):
#         f.write(ri+":\n")
#         f.write(' - text: "'+r+'"\n')
# f.close()

# with open("data_md/intents.md", "w") as f:
#     for i in intents:
#         f.write("  - "+i+"\n")
# f.close()