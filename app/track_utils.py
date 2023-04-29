# Load Database Pkg
import sqlite3

# Fxn To Track Input & Prediction
def create_emotionclf_table():
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('CREATE TABLE IF NOT EXISTS emotionclfTable(rawtext TEXT,prediction TEXT,probability REAL,timeOfvisit TIMESTAMP)')

def add_prediction_details(rawtext,prediction,probability,timeOfvisit):
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('INSERT INTO emotionclfTable(rawtext,prediction,probability,timeOfvisit) VALUES(?,?,?,?)',(rawtext,prediction,probability,timeOfvisit))
		conn.commit()

def view_all_prediction_details():
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('SELECT * FROM emotionclfTable')
		data = c.fetchall()
		return data

# Data 10 cau
# def emotiontest_table_exists():
# 	with sqlite3.connect("database.db") as conn:
# 		c = conn.cursor()
# 		listOfTables = c.execute(
# 		"""SELECT name FROM sqlite_master WHERE type='table' AND name='emotionTestTable'; """).fetchall()
		
# 		if listOfTables == []:
# 			return False
# 		return True

def create_emotiontest_table():
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('CREATE TABLE IF NOT EXISTS emotionTestTable(rawtext TEXT,prediction TEXT,probability REAL, rawemo TEXT)')

def add_predictiontest_details(rawtext,prediction,probability,rawemo):
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('INSERT INTO emotionTestTable(rawtext,prediction,probability,rawemo) VALUES(?,?,?,?)',(rawtext,prediction,probability,rawemo))
		conn.commit()

def view_all_predictiontest_details():
	with sqlite3.connect("database.db") as conn:
		c = conn.cursor()
		c.execute('SELECT * FROM emotionTestTable')
		data = c.fetchall()
		return data