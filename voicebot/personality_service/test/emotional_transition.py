import pickle
import numpy as np

personality="Monica"
type="1"

model = pickle.load(open("../models/type_"+type+"/"+personality+".pickle", 'rb'))

predictions=[]

if type=="1":
    predictions.append(model.predict(np.array([[[0,0.2,0.4],[1,0,0],[0,0.2,0.5],[1,-.6,-.3],[0,0.2,0.3]]], dtype='float64')))


if type=="2":
    predictions.append(model.predict(np.array([[[0.2,0.4],[0,0],[0.2,0.-.2],[-.1,-.2],[0.2,0.3]]], dtype='float64')))


print(predictions)