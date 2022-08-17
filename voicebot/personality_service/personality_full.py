import numpy as np

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
class Personality:

    def __init__(self, thayersInitial, thayersReaction, thayersReset):
        self.thayersInitial=np.around(np.array(self.checkPosition(thayersInitial)), 3)
        self.thayersReset=self.checkReset(thayersReset)
        self.thayersReaction=self.checkReaction(thayersReaction)
        self.thayersPosition=self.thayersInitial
        self.count=0
    


    def updateThayers(self, speakerEmotion):
        speakerEmotion=self.checkPosition(speakerEmotion)
        self.thayersPosition=np.around(self.thayersPosition+self.thayersReaction*np.array(speakerEmotion),3)
        self.checkPosition(self.thayersPosition)
        self.count+=1
        if self.count==self.thayersReset:
            self.count = 0
            self.thayersPosition=self.thayersInitial
    

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


    def checkReaction(self, reaction):
        if (reaction > 1):
            reaction=1
        if (reaction < -1):
            reaction=-1
        return reaction


    def checkReset(self, reset):
        return round(abs(reset))


