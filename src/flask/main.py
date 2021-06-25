# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:01:50 2020

@author: Shreyash
"""
import json
from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
import os
import librosa
import numpy as np
from accModel import ACCModel
from keras.models import model_from_json
def preProcess(audioFile):
    X, sample_rate = librosa.load(audioFile, res_type='kaiser_fast') 
    # We extract mfcc feature from data
    mels = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T,axis=0)    
    mels=np.reshape(mels,(1,16,8,1))
    return mels
model=ACCModel("model.json","model.h5")
app=Flask(__name__)
app.config["IMAGE_UPLOADS"] = "./sounds"
@app.route('/')

@app.route('/upload',methods=["POST"])
@cross_origin()
def upload():
    #return json.dumps({"res":"success","eval":23214})
    if request.files:
        image = request.files["1"]
        image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'mix.wav'))  
        img=preProcess('./sounds/mix.wav')
    return json.dumps({"res":"success","eval":model.predict(img)})
    


if __name__ =="__main__":
    app.run()