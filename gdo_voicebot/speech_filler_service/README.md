# Natural Speech Filllers Service

This service was developed to provide a natural speech fillers feature to the DO voicebot. It works by modifying the GDO's reponse
by inserting natural speech fillers such as "uh", "um" and pauses.
The aim of this service is to give the chatbot a more natural tone of voice.
The number of fillers inserted can be controlled with the help of a level_of_naturalisation variable.

This service is not fully implemented. While filler generation and insertion works, the text-to-speech service is not adapted to
process the reponse from the speech fillers service.

# Data

To perform fillers insertion we utilise data taken from the Movie Dialog Corpus which can be found ['here'](https://www.kaggle.com/Cornell-University/movie-dialog-corpus).

# Preprocessing

We pre-processed the dataset taken from the Movie Dialog Corpus, by substituting all variants of ‘um’ with it and we did the same for ‘uh’. We artificially increased the amount of filler pauses in the data by replacing long dashes and ellipses with a filler pause as well.
