# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 09:51:40 2020

@author: Shreyash
"""

from tensorflow.keras.models import model_from_json
import numpy as np

class ACCModel(object):

    sounds =[
        "air_conditioner", "car_horn", "children_playing", "dog_bark", "drilling", "enginge_idling", "gun_shot","jackhammer", "siren", "street_music"
        ]

    def __init__(self, model_json_file, model_weights_file):
        # load model from JSON file
        with open(model_json_file, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)

        # load weights into the new model
        self.loaded_model.load_weights(model_weights_file)

    def predict(self, img):
        self.preds = self.loaded_model.predict(img)
        return ACCModel.sounds[np.argmax(self.preds)]