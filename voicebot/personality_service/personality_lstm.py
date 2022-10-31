### This class contains the Personality class which maintains and
### updates the state of personalities learned from LSTMs. The 
### variables 'type' and 'personality' can be changed to load a 
### different personality model.

type='2'
personality="Monica"


#                 Arousal |1
#                         |
#                         |
#                         |
#                         |
#   -1                    |                     1
#   ----------------------|----------------------
#                         |                     Valence
#                         |
#                         |
#                         |
#                         |
#                         |
#                         |-1

import numpy as np
import pickle


model = pickle.load(open("models/type_"+type+"/"+personality+".pickle", 'rb'))




class Personality:

    def __init__(self, thayersInitial):
        self.thayersInitial=np.around(np.array(self.checkPosition(thayersInitial)), 3)
        self.thayersPosition=self.thayersInitial
        self.state=[]
    


    def updateThayers(self, speakerEmotion):
        speakerEmotion=self.checkPosition(speakerEmotion)
        global type
        if type=="1":
            speakerEmotion.insert(0,0)
        self.state.append(speakerEmotion)
        global model
        print(self.state)
        print("\n\n\n\n\n")
        self.thayersPosition=model.predict(np.array([self.state], dtype='float64'))[0]
        self.thayersPosition=np.array(self.checkPosition(np.ndarray.tolist(self.thayersPosition*1.5)))
        print(self.thayersPosition)
        thayers_list=[round(float(x), 3) for x in np.ndarray.tolist(self.thayersPosition)]
        print(thayers_list)
        if type=="1":
            thayers_list.insert(0,1)
            self.state.append(thayers_list)
        while len(self.state)>5:
            self.state.pop(0)
    

    def getThayers(self):
        return self.thayersPosition
    

    def checkPosition(self, position):
        if (position[0]>1):
            position[0]=1
        if (position[0]<-1):
            position[0]=-1
        if (position[1]>1):
            position[1]=1
        if (position[1]<-1):
            position[1]=-1
        return position



    def checkReset(self, reset):
        return round(abs(reset))


