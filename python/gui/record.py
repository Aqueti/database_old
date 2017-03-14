#!/usr/bin/python3
import sys 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from RecordGUI import *
from collections import OrderedDict
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from datetime import datetime
from pymongo import MongoClient 
import pymongo
from datetime import date
import json
from array import * 
import subprocess
import ast
from functools import partial
import os
import subprocess
from bson import Binary, Code
from bson.json_util import dumps

"""
# record.py
#
# Must download PyQt5 to run. Go to Ubuntu Software center and type in PyQt5 and download "Development tools for PyQt5"
# Also must download pymongo. Type in pymongo and select "Python3 interface to the MongoDB document-oriented database" 
#
# This is a GUI can record clips, and saves them into a mongo database
# You can use the live button to play the cameras live. The record button will record start/stop time to be saved to the database 
# Or you can access the database and select a clip to start/stop 
#
# Functions to manage the Aqeuti Record interface:
#
# get_data: Function to retrieve and store the start and stop time after pressing the record button 
#
# check_data(labels1, edits1, types1, n, s, v, u): Function to confirm that the clip has a start and stop time after pushing "Send to database"  #						   before sending the clip to the database, if it does, calls send_data 
#
# send_data(self, labels1, edits1, types1, n, s, v, u): Function to put the clip's data in proper JSON format to send it to the mongo database 
#
# remove_tag(self, n, edits, labels, types, tags): Function to remove a tag from the clip's data 
#
# search_db(self, labels, edits, types): Function to search the database for the contents entered. 
#					 If no contents are entered, it returns all clips
#
# start_script(self, results): Function to run start.sh to start playing a selected clip
#
# stop_script(self): Function to run stop.sh to stop playing a selected clip 
#
# live_script(self): Function to run live.sh to go live with the current cameras 
#
# fill_data(self, results): Function to open another window with the selected clip (calls parse_json). Options to start, stop and delete the clip 
#
# delete(self, results, dialog):Function to delete the selected clip 
# 
# parse_json(self, jsonobj, x, y, xx, num, location, labels, edits, types, b): Function to parse the json file from the selected 
#									clip and fill out the new window with the clip's data 
#
# add_tag(self, x, y, location, tags, labels, edits, types, n, x2): Function to add another tag for the clip's json data 
#
############################################################

"""

class MainScreen():

	record = False
	start_time = 0
	stop_time = 0
	tagslist = list()
	n = 0
	tagslist2 = list()
	n2 = 0

	def __init__(self):

		QMainWindow.__init__(self)


#
#		self.ui = RecordGUI()
#		self.ui.setupUi(self)	
#		edits = list()
#		labels = list()
#		types = list()
#		edits1 = list()
#		labels1 = list()
#		types1 = list()
#		with open("cliptemplate.json") as json_file:
#			json_data = json.load(json_file, object_pairs_hook = OrderedDict)
#			self.parse_json(json_data, 50, 70, 200, 0, self.ui.tab, labels, edits, types, True)
#			self.ui.send.clicked.connect(partial(self.check_data, labels, edits, types, 0, "{ ", 0, ""))
#			self.parse_json(json_data, 50, 70, 200, 0, self.ui.tab2, labels1, edits1, types1, False)
#			self.ui.search.clicked.connect(partial(self.search_db, labels1, edits1, types1))
#
#		
#		self.ui.record.clicked.connect(self.get_data)
#		self.ui.live.clicked.connect(self.live_script)
#

	"""
	#Retrieves the startTime and stopTime after hitting the record button
	"""
	def get_data(self):
		if(self.record == False):		
			self.start_time = datetime.now().time()
			self.start_time = self.start_time.isoformat()
			self.ui.start.setText(self.start_time)
			self.record = True
		elif(self.record == True):
			self.stop_time = datetime.now().time()
			self.stop_time = self.stop_time.isoformat()
			self.ui.stop.setText(self.stop_time)
			self.record = False
	

	"""
	#Confirms that there is a start and stop time before sending clip to database
	"""
	def check_data(self, labels1, edits1, types1, n, s, v, u):
		if(self.start_time == 0):
			self.ui.error.setText('Must record a clip to send')
			self.ui.error.show()
		elif(self.stop_time == 0): 
			self.ui.error.setText('Must stop recording to send clip')
			self.ui.error.show()
		else:
			self.send_data(labels1, edits1, types1, n, s, v, u)

	"""
	# Puts the clip's data in proper JSON format and sends it to the database
	"""
	def send_data(self, labels1, edits1, types1, n, s, v, u):

		m = 0 
		while(n<len(labels1)):
			if(type(edits1[n])!=str):
				s+='"'
				s+= str(labels1[n].text())
				s+='"'
				s+= ': '
				if( (types1[n] != "True") & (types1[n] != "False") & (types1[n] != "int") & (types1[n] != "integer") & (types1[n] != "double") & (types1[n] != "float") & (types1[n] != "null")):
					m = 1
					s+='"'
				elif( ((str(edits1[n].text()) == "string")) | ((str(edits1[n].text()) == "int")) | ((str(edits1[n].text()) == "double"))):
					m = 1
					s+= '"'
				elif( ((str(labels1[n].text()) == "startTime")) | ((str(labels1[n].text()) == "stopTime"))):
					m = 1
					s += '"'
				s+= str(edits1[n].text())
				if(m == 1):
					s+='"'
				m = 0
				if (n + 1 != len(labels1) ):
					if( (edits1[n + 1] != "}") ): 
						
						s+= ' , '
					
			elif(edits1[n]=="null"):
				s+='"'
				s+= str(labels1[n].text())
				s+='"'
				s+= ': '
				s+= '{ \n'
				n+=1
				labels1, edits1, types1, n, s= self.send_data(labels1, edits1, types1, n, s, v, u)
				v = 1
				
			elif(edits1[n]=="}"):
				if(n+1 != len(labels1) ):
					s+='\n'					
					s+='} '
					if((edits1[n+1]!= "}")):					
						s+=', \n'
			elif(edits1[n]=="listnull"):
				s+= '"'
				s+= str(labels1[n - 1].text())
				s+= '"'
				s+= ':'
				s+= '[ \n'			
				s+= '{ \n'
				n+=1
				labels1, edits1, types1, n, s= self.send_data(labels1, edits1, types1, n, s, v, u)
				v=1
				s += ']'
					
				if(n + 1 < len(labels1)):
					if((i == 1) & (edits1[n + 1]!= "}")):
						s+=','
			elif(edits1[n]=="list"):
				s+= '"'
				s+= str(labels1[n].text())
				s+= '"'
				s+= ':'
				s+= '[ '

				while(labels1[n+1] == ""):
					n+=1
					s+= '"'
					s+=str(edits1[n].text())
					s+='"'
					if(labels1[n+1] == ""):
						s+=','
					else:
						s+=']'
						if(edits1[n+1] != "}"):
							s+=','
			if(n<len(labels1)):
				if(type(labels1[n])!=str):
					if(labels1[n].text() == "version"):
						self.v = edits1[n].text()			
			n+=1
		
		if(v==0):
			s+='}'
		file = 'something.json'
		with open(file, "w") as outfile:
			outfile.write(s)
		if(n==len(labels1)+1):
			save = json.loads(s)
			client = pymongo.Connection()
			db = client.clips
			if(u ==""):
				db['clip'].insert(save)
			else:
				db['clip'].remove({'_id': u})
				db['clip'].insert(save) 
				

		return labels1, edits1, types1, n, s




	"""
	# Removes a tag from the clip's data 
	"""
	def remove_tag(self, n, edits, labels, types, tags):
		edits[n].deleteLater()
		del edits[n]
		del labels[n]
		del types[n]
		tags.pop()

	"""
	# Searches the database for the contents entered. If no contents are entered, it returns all clips
	"""
	def search_db(self, labels, edits, types):
		x = 0
		y = 0
		z = 0
		j = 0
		d = ""
		while (x < len(edits)): 
			#if((type(edits[x])==str) & (type(labels[x])==str)):
			#	d+=""
			if(type(edits[x])!=str):			
				if((edits[x].text()!="")&(labels[x]!="")):
					if(y==0):
						d+= '{'
						y+=1
					if(z==1):
						print('1')
						d+=', '
						z = 0
					if(type(labels[x])!=str):
						if((labels[x].text()!="version") & (labels[x].text()!="type") & (labels[x].text()!="tags")):
							d+= '"clip.' + labels[x].text() + '": "' + edits[x].text() + '"'
							z = 1



	
			elif(type(labels[x])!=str):
				
				if(labels[x].text()=="tags"):
					
					x2 = x+1
					while(x2<len(edits)):
						if(labels[x2]==""):
							if(edits[x2]!="}"):
								if(edits[x2].text()!=""):
									if(y==0):
										d+= '{'
										y+=1
									if(z==1):
										d+=","
									d+= '"clip.' + labels[x].text() + '": "' + edits[x2].text() + '"'	
									z = 1
						x2+=1

					
			if(x+1 == len(edits)):
				if(d!=""):
					d+=' }'
			x+=1

		dialog = QDialog()
		dialog.ui = Ui_Dialog()
		dialog.ui.setupUi(dialog)
		
		xc = 0
		yc = 0 
		aresults = list()
		editresults = list()
		print(d)
		if(d!=""):
			doc = ast.literal_eval(d)
			client = MongoClient()
			coll = client.clips
			cursor = coll['clip'].find(doc)
			s = ""
			for result_object in cursor:
				aresults.insert(xc, QtWidgets.QTextEdit(dialog))
				dialog.ui.formLayout.setWidget(xc, QtWidgets.QFormLayout.FieldRole, aresults[xc])
				aresults[xc].setText(str(result_object))
				aresults[xc].show()
				editresults.insert(xc, QtWidgets.QPushButton(dialog))
				dialog.ui.formLayout.setWidget(xc, QtWidgets.QFormLayout.LabelRole, editresults[xc])
				editresults[xc].setText(str("select"))
				editresults[xc].clicked.connect(partial(self.fill_data, result_object))
				yc += 45
				xc+=1
			
		else:
			client = MongoClient()
			coll = client.clips
			cursor = coll['clip'].find()		
			s = ""
			for result_object in cursor:
				aresults.insert(xc, QtWidgets.QTextEdit(dialog))
				dialog.ui.formLayout.setWidget(xc, QtWidgets.QFormLayout.FieldRole, aresults[xc])
				aresults[xc].setText(str(result_object))
				aresults[xc].show()
				editresults.insert(xc, QtWidgets.QPushButton(dialog))
				dialog.ui.formLayout.setWidget(xc, QtWidgets.QFormLayout.LabelRole, editresults[xc])
				editresults[xc].setText(str("select"))
				editresults[xc].clicked.connect(partial(self.fill_data, result_object))
				yc+=45
				xc+=1

		dialog.exec_()

	"""
	# Starts playing the selected clip by running start.sh 
	"""
	def start_script(self, results):
		os.system('chmod +x start.sh')
		subprocess.call(['./start.sh', str(results)])

	"""
	# Stops playing the selected clip by running stop.sh
	"""
	def stop_script(self):
		os.system('chmod +x stop.sh')
		os.system('./stop.sh')

	"""
	# Plays the cameras live by running live.sh 
	"""
	def live_script(self):
		os.system('chmod +x live.sh')
		subprocess.call('./live.sh')

	"""
	#Opens another window with the selected clip. Options to start, stop and delete
	"""
	def fill_data(self, results):

		dialog = QDialog()
		dialog.ui = Ui_Dialog2()
		dialog.ui.setupUi(dialog)
		labels = list()
		edits = list()
		types = list()
		y, x, x2, n = self.parse_json(results, 50, 50, 130, 0, dialog, labels, edits, types, "")
		start = QtWidgets.QPushButton(dialog)
		start.setGeometry(QtCore.QRect(x+20, y, 100, 27))
		start.setText("start")
		start.clicked.connect(partial(self.start_script, results))
		stop = QtWidgets.QPushButton(dialog)
		stop.setGeometry(QtCore.QRect(x+20, y+35, 100, 27))
		stop.setText("stop")
		stop.clicked.connect(partial(self.stop_script))
		delete = QtWidgets.QPushButton(dialog)
		delete.setGeometry(QtCore.QRect(x+20, y+70, 100, 27))
		delete.setText("delete")
		delete.clicked.connect(partial(self.delete, results, dialog))
		update = QtWidgets.QPushButton(dialog)
		update.setGeometry(QtCore.QRect(x+20, y+100, 100, 27))
		update.setText("update")
		update.clicked.connect(partial(self.send_data, labels, edits, types, 0, "{", 0, results['_id']))
		dialog.exec_()


	"""
	#deletes the selected clip
	"""
	def delete(self, results, dialog):
		client = MongoClient()
		coll = client.clips
		cursor = coll['clip'].remove({'_id': results['_id']})	
		dialog.close()
	
	"""
	#Fills out the window with the selected clip's json data 
	"""
	def parse_json(self, jsonobj, x, y, xx, num, location, labels, edits, types, b):
		n = num
		jsonthing = dumps(jsonobj)
		json_data = json.loads(jsonthing, object_pairs_hook = OrderedDict)
		aType = type(json_data)
		x1 = x
		y1 = y
		x2 = xx

		for key in json_data.keys():
			if(key!='_id'):			
				if((b==True) & ((key=="version") | (key=="type"))):
					labels.insert(n, QtWidgets.QLabel(location))
					labels[n].setText(key)
					labels[n].hide()
					edits.insert(n, QtWidgets.QLabel(location))
					edits[n].setText(json_data[key])
					edits[n].hide()
					types.insert(n, "string")
					n+=1
				elif(((b==False)|(b=="")) & ((key=="version") | (key=="type"))):
					labels.insert(n, QtWidgets.QLabel(location))
					labels[n].setText(key)
					labels[n].setGeometry(QtCore.QRect(x1, y1, 110, 27))
					edits.insert(n, QtWidgets.QLabel(location))
					edits[n].setText(json_data[key])
					edits[n].setGeometry(QtCore.QRect(x2, y1, 110, 27))
					types.insert(n, "string")
					y1+=30
					n+=1
				else:
					labels.insert(n, QtWidgets.QLabel(location))
					labels[n].setGeometry(QtCore.QRect(x1, y1, 110, 27))
					labels[n].setText(key)
					if(type(json_data[key])==aType):
						edits.insert(n, "null")
						types.insert(n, "null")
						y1+=30
						n+=1			
						y1, x1, x2, n = self.parse_json(json_data[key], x1+50, y1, x2+50,  n, location, labels, edits, types, b)

					elif(type(json_data[key])==list):
						edits.insert(n, "list")
						types.insert(n, "null")
						y3 = y1
						n+=1
						x = 0 
						for item in json_data[key]:
							if(type(item) ==aType):
								labels.insert(n, "")
								edits.insert(n, "listnull")
								types.insert(n, "null")
								y1+=30
								n+=1 
								y1, x1, x2, n = self.parse_json(item, x1+50, y1, x2+50, n, location, labels, edits, types, b)
							else:
								if(x == 0):
									self.add = QtWidgets.QPushButton(location)
									self.add.setGeometry(QtCore.QRect(x1-70, y3, 60, 27))
									tags = list()
									self.add.setText("add tag")
									self.add.clicked.connect(partial(self.add_tag, x2+160, y3, location, tags, labels, edits, types, n, x1-70))	
									x+=1
								labels.insert(n, "")
								types.insert(n, "nul")
								edits.insert(n, QtWidgets.QLineEdit(location))
								edits[n].setGeometry(QtCore.QRect(x2, y3, 140, 27))
								if(b==""):
									edits[n].setText(item)
								n+=1
								y3+=30
								y1=y3		
					else:	
						if((key=="startTime") & (b ==True)):
							edits.insert(n, self.ui.start)	
							edits[n].setGeometry(QtCore.QRect(x2, y1, 140, 27))
						elif((key=="stopTime")&(b==True)):
							edits.insert(n, self.ui.stop)		
							edits[n].setGeometry(QtCore.QRect(x2, y1, 140, 27))
						elif((key=="date")&(b==True)):
							edits.insert(n, QtWidgets.QLabel(location))
							edits[n].setGeometry(QtCore.QRect(x2, y1, 140, 27))
							edits[n].setText(str(date.today()))
						else:
							edits.insert(n, QtWidgets.QLineEdit(location))
							edits[n].setGeometry(QtCore.QRect(x2, y1, 140, 27))
							if(b==""):
								edits[n].setText(str(json_data[key]))
						if((key=='systemID') & (b==True)):
							edits[n].setText(str(json_data[key]))
						types.insert(n, str(json_data[key]))
						n+=1
						y1+=30
				
		labels.insert(n, "")
		edits.insert(n, "}")
		types.insert(n, "null")
		n+=1

		return (y1, x1-50, x2-50, n)

	"""
	# Adds a tag to the clip's json data 
	"""
	def add_tag(self, x, y, location, tags, labels, edits, types, n, x2):
		edits.insert(n, QtWidgets.QLineEdit(location))
		edits[n].setGeometry(QtCore.QRect(x+(130*len(tags)), y, 110, 27))
		edits[n].show()	
		labels.insert(n, "")
		types.insert(n, "string")
		tags.insert(0,1)
		removetag = QtWidgets.QPushButton(location)
		removetag.setGeometry(QtCore.QRect(x2-40, y+30, 110, 27))
		removetag.setText("remove tag")
		removetag.show()
		removetag.clicked.connect(partial(self.remove_tag, n, edits, labels, types, tags))
			
app = QApplication(sys.argv)
window = MainScreen()
window.show()
sys.exit(app.exec_())
