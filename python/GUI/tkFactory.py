#!/usr/bin/python3

import json
from tkinter import *
from tkinter import ttk


##@brief class for creating TK GUIs on the fly
class tkFactory:
   running = True
   components = {}
   loopCallback = ""
   loopDuration = 1000
   
   ##@brief intialize the main window and start the mainloop
   def __init__(self, template, width, height ):
      self.window = Tk()
      self.window.title(template["name"])
      self.window.geometry(str(width)+"x"+str(height))
      self.name = "root"

   ##@brief starts execution
   def start(self, callback, duration ):
      self.loopCallback = callback
      self.loopDuration = duration
      self.run()

   ##@brief Function that executes callback and resumes execution loop
   def run(self): 
      if self.running == True:
         self.loopCallback()
         self.window.after( self.loopDuration, self.run)
         self.window.mainloop()

   ##@brief function to add a new object to the GUI. 
   def addObject( self, name, template, value="", parent="" ):
      count = 0
      children = []
      if parent == "":
         parent = self.window

      if template["type"] == "dictionary" or template["type"] == "template":
         child = self.addDictionary( template, parent, value )
      if template["type"] == "string":
         child = self.addTextBox( name, template, parent, value )
      else:
         return 0


      children.append( child)
      return children

   ##@brief create a new dictionary form 
   def addDictionary( self, template, parent, value={} ):
      children = []
      print("Adding dictionary")

      frame = Frame(parent)
      frame.pack( expand = True )

      #add a label at the top
      if "name" in template:
         child = self.addLabel(template["name"], frame)
         children.append(child)

      #add the data
      if "data" in template:
         for k, v in template["data"].items():
             child = self.addObject( k, template["data"][k], value, frame )
             children.append(child)
      return frame

   ##@brief adds a label
   def addLabel(self, labelText, parent, pos=LEFT ):
      frame = Frame( parent)
      frame.pack()
      label = Label( frame, text=labelText )
      label.pack( side = pos)
      return frame


   ##@brief add a text box
   def addTextBox( self, labelText, template, parent, value=""):
      if "edit" in template:
         print( str(template["edit"]))
         editFlag = template["edit"]
         print("Edit found and is"+str(editFlag))
      else:
         print("Edit found and False")
         editFlag = True

      frame = Frame( parent)
      frame.pack()
      frame.pack(fill = X)
 
      label = Label( frame, text=labelText)
      label.pack( side = LEFT)
      entry = Entry( frame )
      entry.pack( expand = True)

      if not editFlag:
         entry.config(state = DISABLED )

      return frame
   

   ##@brief add a frame dictionary
   def addButton( self, text, callback ):
      print("Adding button")
   
      
      
