# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 23:39:32 2021

@author: Shreyash
"""
import json
from flask import Flask,jsonify,request
from flask_cors import CORS, cross_origin
import os
import librosa
import numpy as np
import os
import librosa
import math
import json
import numpy as np
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from pydub import AudioSegment
from scipy.special import softmax
from sklearn.metrics import confusion_matrix





param_path="C:/Users/Shreyash/Desktop/git/Acoustic-FastGRNN/examples/tf-examples/FastCells/FastGRNNResults/2021-04-20T21-15-53/"
SAMPLE_RATE = 22050
app=Flask(__name__)
app.config["audio"] = "./sounds"

def get_mfcc(n_mfcc = 13, n_fft = 2048, hop_length = 512, num_segments = 5):
    mfccs=[]
    num_samples_per_segment = 13230
    expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)  # rounding
    # print(expected_num_mfcc_vectors_per_segment,num_samples_per_segment)  
    signal, sr = librosa.load('./sounds/mix.wav')
    for s in range(num_segments):
        start_sample = num_samples_per_segment * s  # starting point for each segment
        finish_sample = start_sample + num_samples_per_segment  # end point
                
        mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample],
                                    sr=sr,
                                    n_fft=n_fft,
                                    n_mfcc=n_mfcc,
                                    hop_length=hop_length)
        mfcc = mfcc.T
        mfccs.append(mfcc);
    return mfccs
def get_vars():
    m={}
    m["U"]=np.load(param_path+"U.npy")
    m["W"]=np.load(param_path+"W.npy")
    m["zeta"]=np.load(param_path+"zeta.npy")
    m["nu"]=np.load(param_path+"nu.npy")
    m["B_g"]=np.load(param_path+"Bg.npy")
    m["B_h"]=np.load(param_path+"Bh.npy")
    m["FC"]=np.load(param_path+"FC.npy")
    m["FCbias"]=np.load(param_path+"FCbias.npy")
    m["mean"]=np.load(param_path+"mean.npy")
    m["std"]=np.load(param_path+"std.npy")
    return m
def sigmoid(val):
    return (1/(1+np.exp(-val)))
def predict(X):
    preds=[]
    # np.shape(X)
    classes=os.listdir('C:/Users/Shreyash/Desktop/git/Acoustic-FastGRNN/AudioDS2_test/')
    for segment in X:
        h_tm1=np.zeros((1,26))
        segment=(segment-m["mean"])/m["std"]
        for x_t in segment:
            x_t = np.array(x_t)
            x_t=x_t.reshape((1,13));
            z_t=sigmoid(np.dot(x_t,m["W"]) + np.dot(h_tm1,m["U"]) + m["B_g"])
            h_t_=np.tanh(np.dot(x_t,m["W"]) + np.dot(h_tm1,m["U"]) + m["B_h"])
            h_t=z_t*h_tm1+(sigmoid(m["zeta"])*(1-z_t)+sigmoid(m["nu"]))*h_t_
            h_tm1=h_t;
        
        preds.append(np.argmax(softmax(np.dot(h_t,m["FC"])+m["FCbias"])))
    for i in range(len(preds)):
        preds[i]=classes[preds[i]];
    return preds
m=get_vars()
m["mean"]=m["mean"].reshape((26,13));
m["std"]=m["std"].reshape((26,13));
@app.route('/')

@app.route('/upload',methods=["POST"])
@cross_origin()
def upload():
    #return json.dumps({"res":"success","eval":23214})
    print(request.files)
    if request.files:
        audio_file= request.files["1"]
        audio_file.save(os.path.join(app.config["audio"], 'mix.wav'))
        DURATION = (len(AudioSegment.from_wav('./sounds/mix.wav'))/1000)  
        mfccs=get_mfcc(num_segments=int(DURATION/.6))
        preds=predict(mfccs)
        # print(preds)
        ret=""
        for i in preds:
            ret+=' '+str(i)
        # img=preProcess('./sounds/mix.wav')
    return json.dumps({"res":"success","preds":ret.strip()})

if __name__ =="__main__":
    app.run()