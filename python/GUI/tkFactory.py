#!/usr/bin/python3

import json
from tkinter import *
from tkinter import ttk

##@brief adds a label
def addLabel(labelText, parent, pos=LEFT ):
   frame = Frame( parent)
   frame.pack()
   label = Label( frame, text=labelText )
   label.pack( side = pos)
   return frame

##
# @brief    function to add a new object to the GUI. 
#
# This function adds an object to the widget pointed to by parent. 
##
def addObject( parent, key, template, value="" ):
   if "edit" in template:
      editFlag = template["edit"]
   else:
      editFlag = True

   if template["type"] == "dictionary" or template["type"] == "template":
      child = DictionaryNode( parent, key, template, value )
   elif template["type"] == "string":
      if "value" in template:
         value = template["value"]
      else:
         value = "unknown"
         child = TextBoxNode( parent, key, value, editFlag)
   else:
      return 0

   return 1

##@brief Create a dictionary object
class DictionaryNode:
   def __init__(self, parent, key, template, value ):
      children = []
      frame = Frame(parent)
      frame.pack( expand = True )

      #add a label at the top
      child = addLabel(key, frame)
      children.append(child)

      #add the data
      if "data" in template:
         for k, v in template["data"].items():
             child = addObject( frame, k, template["data"][k], value )
             children.append(child)

      if "edit" in template:
         editFlag = template["edit"]
      else:
         editFlag = False

      if editFlag is True:
         child = ButtonNode( "AddObject", "Add Key", frame ) 
#         children.append(child)

   def updateFunction( self ):
      print("Button Press")

##@brief Class for a button node 
class ButtonNode():     
   def __init__(self, key, text, parent):
      print("Key: "+key)
      self.key = key
      self.parent = parent 

      frame = Frame(parent)
      frame.pack()
      self.button = Button( frame, text=text, command = lambda: self.pressCallback())
      self.button.pack()

   ##@brief callback fro when the button is pressed
   def pressCallback( self ):
      print("Button pressed:")

##@brief class for a text box
class TextBoxNode:
   def __init__( self, parent, key, value, edit = True ):
      self.parent = parent
      frame = Frame( self.parent)
      frame.pack()
      frame.pack(fill = X)
   
      label = Label( frame, text=key)
      label.pack( side = LEFT)
      self.entry = Entry( frame )
      self.entry.insert(0, value)
      self.entry.pack( expand = True)

      #if we are not editing, disable
      if not edit:
         self.entry.config(state = DISABLED )

   ##@brief function to update parent (and return data)
   def updateData(self):
      value = self.entry.get()
      self.parent.data[key] = value
      return value


##@brief Class for a popup window that allows creation of a new dialog
class AddDialog:
    ##@Initialization function
    def __init__(self, parent ):
      #Add callback. 
      self.parent = parent
      self.top = Toplevel(self.parent)
      frame = Frame( self.top )
      frame.pack()

      #create a drop down with the supported type
      widgetList = ["array", "dictionary", "string", "integer", "double"] 
      self.var = StringVar(frame)
      self.var.set("string")
      self.w = OptionMenu(frame, self.var, *widgetList)
      self.w.pack()

      #Creatre a cancel button
      cb = Button(self.top, text="Cancel", command=self.cancel)
      cb.pack(pady=5)

      #Creatre an OK button
      b = Button(self.top, text="OK", command=self.ok)
      b.pack(pady=5)

    def cancel(self):
        print("Cancelling")
#        self.callback(self.e.get())
        self.top.destroy()

    def ok(self):
        data = {}
        data["type"] = self.var.get()
        self.parent.data.append(data)
        self.top.destroy()


##@brief class for creating TK GUIs on the fly
class tkFactory:
   running = True
   root       = -1
   components = {}
   loopCallback = ""
   loopDuration = 1000
   buttonCount = 0

   
   ##@brief intialize the main window and start the mainloop
   def __init__(self, template, width, height ):
      self.window = Tk()
      self.window.title(template["name"])
      self.window.geometry(str(width)+"x"+str(height))
      self.window.data = {}

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
   def generate( self, name, template, value="" ):
      self.name = name
      self.window.data = addObject( self.window, self.name, template, value )


   ##@brief dictionary button press
   def addButtonPress(self, parent):
      self.buttonCount = self.buttonCount+1
      print( str(self.buttonCount ))
      d = AddDialog(parent)
      

   ##@brief add a new dictionary item
   def addItem( self, parent ):
      print("Adding item")
      

   ##@brief add a button
   def addButton( self, buttonText, callback, parent):
      frame = Frame(parent)
      frame.parent = parent
      frame.pack()
      button = Button( frame, text=buttonText, command = lambda: callback(frame))
      button.pack()

      return frame




   ##@brief add a text box
   def addTextBox( self, labelText, template, parent, value=""):
      if "edit" in template:
         print( str(template["edit"]))
         editFlag = template["edit"]
         print("Edit found and is "+str(editFlag))
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
   

