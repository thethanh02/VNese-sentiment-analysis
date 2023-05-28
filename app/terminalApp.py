# EDA Pkgs
import pandas as pd 
import numpy as np 

# Utils
import ktrain
predictor = None
def load_predictor():
	global predictor
	predictor = ktrain.load_predictor('./saved_model')

# Utils
from utils import my_normalize_text
from track_utils import *

# Fxn
def predict_emotions(docx):
	results = predictor.predict([docx])
	return results[0]

def get_prediction_proba(docx):
	results = predictor.predict_proba([docx])
	return results

emotions_emoji_dict = {'thông tin':'😐', 'hạnh phúc':'😊', 'buồn bã':'😔', 'sợ hãi':'😱', 'ngạc nhiên':'😮', 'phẫn nộ':'😠'}

if __name__ == '__main__':
    load_predictor()
    while True:
        raw_text = input('Input: ')
        handled_text = my_normalize_text(raw_text)
        prediction = predict_emotions(handled_text)
        probability = get_prediction_proba(handled_text)
        emoji_icon = emotions_emoji_dict[prediction]
        print('Handled text: ', handled_text)
        print("{}:{}".format(prediction,emoji_icon))
        print("Confidence: {}%".format(np.max(probability)*100))