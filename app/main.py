# Core Pkgs
import streamlit as st 
import altair as alt

# EDA Pkgs
import pandas as pd 
import numpy as np 
from datetime import datetime

# Utils
import ktrain
predictor = None
def load_predictor():
	global predictor
	predictor = ktrain.load_predictor('./saved_model')

# Utils
from utils import my_normalize_text
from track_utils import *

from googletrans import Translator
translator = Translator()

import sqlite3
def emotiontest_table_exists():
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		listOfTables = c.execute(
		"""SELECT name FROM sqlite_master WHERE type='table' AND name='emotionTestTable'; """).fetchall()
		
		if listOfTables == []:
			return False
		return True
	
def load_testdata():
	check = emotiontest_table_exists()
	if not check:
		create_emotiontest_table()
		dataset = pd.read_csv("./test10cau.csv")
		for i in range(12):
			raw_text = dataset['Text'][i]
			probability = get_prediction_proba(raw_text)
			add_predictiontest_details(raw_text, predictor.predict(raw_text), float(np.max(probability)), dataset['Emotion'][i])

# Fxn
def predict_emotions(docx):
	results = predictor.predict([docx])
	return results[0]

def get_prediction_proba(docx):
	results = predictor.predict_proba([docx])
	return results

emotions_emoji_dict = {'thông tin':'😐', 'hạnh phúc':'😊', 'buồn bã':'😔', 'sợ hãi':'😱', 'ngạc nhiên':'😮', 'phẫn nộ':'😠'}

# Main Application
def main():
	st.title("Emotion Classifier App")
	menu = ["Home","Monitor"]
	choice = st.sidebar.selectbox("Menu",menu)
	load_predictor()
	load_testdata()
	create_emotionclf_table()
	if choice == "Home":
		st.subheader("Home-Emotion In Text")

		with st.form(key='emotion_clf_form'):
			raw_text = st.text_area("Type Here")
			submit_text = st.form_submit_button(label='Submit')

		if submit_text:
			col1,col2  = st.columns(2)
			handled_text = my_normalize_text(raw_text)
			# Apply Fxn Here
			prediction = predict_emotions(handled_text)
			probability = get_prediction_proba(handled_text)
			# print(prediction)
			add_prediction_details(raw_text,prediction,float(np.max(probability)),datetime.now())
			
			with col1:
				st.success("Handled Text")
				st.write(handled_text)

				st.success("Prediction")
				emoji_icon = emotions_emoji_dict[prediction]
				st.write("{}:{}".format(prediction,emoji_icon))
				st.write("Confidence: {}%".format(np.max(probability)*100))


			with col2:
				st.success("Prediction Probability")
				proba_df = pd.DataFrame(probability,columns=predictor.get_classes())
				proba_df_clean = proba_df.T.reset_index()
				proba_df_clean.columns = ["emotions","probability"]

				fig = alt.Chart(proba_df_clean).mark_bar().encode(
					x='emotions',
					y='probability',
					color='emotions')
							
				st.altair_chart(fig,use_container_width=True)


	elif choice == "Monitor":
		st.subheader("Monitor App")

		with st.expander("Test Metrics"):
			df_emotions = pd.DataFrame(view_all_predictiontest_details(),columns=['RawText','Prediction','Probability','RawEmotion'])
			st.dataframe(df_emotions)
			df_emotions['index'] = df_emotions.index

			chart = alt.Chart(df_emotions).mark_bar(width=20).encode(
				x='index',
				y='Probability',
				color='Prediction'
			)
			st.altair_chart(chart,use_container_width=True)

		with st.expander('Emotion Classifier Metrics'):
			df_emotions = pd.DataFrame(view_all_prediction_details(),columns=['Rawtext','Prediction','Probability','Time_of_Visit'])
			st.dataframe(df_emotions)

			prediction_count = df_emotions['Prediction'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
			pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction',y='Counts',color='Prediction')
			st.altair_chart(pc,use_container_width=True)	


if __name__ == '__main__':
	main()