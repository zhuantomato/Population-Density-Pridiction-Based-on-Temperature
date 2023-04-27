import pickle
import numpy as np
import pandas as pd
import tensorflow as tf

#在fix_temp上部署模型
def fixtempPred(fixtemp):
    scaler = pickle.load(open('WebGUI\scaler.pkl', 'rb'))
    fixtemp = scaler.transform(fixtemp)
    result_fixtemp = model.predict(fixtemp)
    return result_fixtemp

def fixhourPred(fixhour,temp):
    scaler = pickle.load(open('WebGUI\scaler.pkl', 'rb'))
    fixhour = scaler.transform(fixhour)
    result_fixhour = model.predict(fixhour)
    return result_fixhour

fixtemp = pd.read_csv('Visualising/Analysis/fix_temp.csv')
fixhour = pd.read_csv('Visualising/Analysis/fix_hour.csv')
fixtemp.columns = ['temperature','latitude','longitude', 'is_weekend', 'hour']
fixhour.columns = ['temperature','latitude','longitude', 'is_weekend', 'hour']
model = tf.keras.models.load_model('AutoAdjustedModels\DNN\DNNSimple.h5')

result_fixtemp = pd.DataFrame(fixtempPred(fixtemp))
result_fixhour = pd.DataFrame(fixhourPred(fixhour,fixhour['temperature']))

fixtempData = pd.concat([result_fixtemp, fixtemp], axis=1)
fixhourData = pd.concat([result_fixhour, fixhour], axis=1)

fixtempData.to_csv("Visualising/Visulising/fixtempData.csv", header=['status','temperature','latitude','longitude', 'is_weekend', 'hour'], index=False)
fixhourData.to_csv("Visualising/Visulising/fixhourData.csv", header=['status','temperature','latitude','longitude', 'is_weekend', 'hour'], index=False)

