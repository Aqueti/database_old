#!/usr/bin/python3

import json
import tkinter as tk
from tkinter import ttk

##@brief adds a label
def addLabel(labelText, parent, pos=tk.LEFT ):
   frame = tk.Frame( parent)
   frame.pack()
   label = tk.Label( frame, text=labelText )
   label.pack( side = pos)
   return frame

##@brief class to handle a group of frames
class FrameGroup(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.all_instances = []
        self.counter = 0

    def Add(self):
        self.counter += 1
        name = "tk.Frame %s" % self.counter 
        subframe = Subframe(self, name=name)
        subframe.pack(side="left", fill="y")
        self.all_instances.append(subframe)

    def Remove(self, instance):
        # don't allow the user to destroy the last item
        if len(self.all_instances) > 1:
            index = self.all_instances.index(instance)
            subframe = self.all_instances.pop(index)
            subframe.destroy()

    def HowMany(self):
        return len(self.all_instances)

    def ShowMe(self):
        for instance in self.all_instances:
            print(instance.get())

##@brief Subframe class
class Subframe(tk.Frame):
    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.e1 = tk.Entry(self)
        self.e2 = tk.Entry(self)
        self.e3 = tk.Entry(self)
        label = tk.Label(self, text=name, anchor="center")
        add_button = tk.Button(self, text="Add", command=self.parent.Add)
        remove_button = tk.Button(self, text="Remove", command=lambda: self.parent.Remove(self))

        label.pack(side="top", fill="x")
        self.e1.pack(side="top", fill="x")
        self.e2.pack(side="top", fill="x")
        self.e3.pack(side="top", fill="x")
        add_button.pack(side="top")
        remove_button.pack(side="top")

    def get(self):
        return (self.e1.get(), self.e2.get(), self.e3.get())

##@brief Class for a popup window that allows creation of a new dialog
class AddDialog:
    ##@Initialization function
    def __init__(self, parent, callback ):
      #Add callback. 
      self.callback = callback
      self.parent = parent
      self.top = tk.Toplevel(self.parent)
      frame = tk.Frame( self.top )
      frame.pack()

      self.keyTextBox = TextBoxNode( frame, "key:", "", True)

      #create a drop down with the supported type
      widgetList = ["array", "dictionary", "string", "integer", "double"] 
      self.typeField = tk.StringVar(frame)
      self.typeField.set("string")
      self.typeOption = tk.OptionMenu(frame, self.typeField, *widgetList)
      self.typeOption.pack()

      self.editFlag = tk.IntVar()
      self.editButton = tk.Checkbutton(frame, text="Edit", variable=self.editFlag ) 
      self.editButton.select()
      self.editButton.pack()

      self.requiredFlag = tk.IntVar()
      self.requiredButton = tk.Checkbutton(frame, text="required", variable=self.requiredFlag )
      self.requiredButton.deselect()
      self.requiredButton.pack()

      self.autoFlag = tk.IntVar()
      self.autoButton = tk.Checkbutton(frame, text="auto", variable=self.autoFlag )
      self.autoButton.deselect()
      self.autoButton.pack()


      #Creatre a cancel button
      cb = tk.Button(self.top, text="Cancel", command=self.cancel)
      cb.pack(pady=5)

      #Creatre an OK button
      b = tk.Button(self.top, text="OK", command=self.ok)
      b.pack(pady=5)

    def cancel(self):
        print("Cancelling")
        self.top.destroy()

    def ok(self):
        data             = self.keyTextBox.getData()
        data["type"]     = self.typeField.get()
        data["edit"]     = bool(self.editFlag.get())
        data["required"] = bool(self.requiredFlag.get())
        data["auto"]     = bool(self.autoFlag.get())

        self.callback(data)
        self.top.destroy()


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
         value = ""

      child = TextBoxNode( parent, key, value, editFlag)
      parent.pack()
   else:
      return 0

   return 1

##@brief base class for extracting data from components
class BaseObject:
   data = {}
   parent = None

   ##@brief Initialization function specifies the key
   def __init__(self, key ):
      self.key = key

   ##@brief function to update data
   def updateData( self, key, value ):
      self.data[key] = value
     
      if self.parent:
         parent.updateData( key, self.data )

##@brief Create a dictionary object
#
# @param parent reference to the parent tk object
# @param key key that will map to the key/value pair
# @param template template object that defines what information should be in the dictionary
# @param value an object that matches the template teh contains the object value(s)
class DictionaryNode(BaseObject):
   data = {}
   def __init__(self, parent, key, template, value ):
      BaseObject.__init__(self, key )

      self.frame = tk.Frame(parent)
      self.frame.pack( expand = True )

      self.dataFrame = tk.Frame(self.frame)
      self.dataFrame.pack( expand = True )

      #add a label at the top
      addLabel(key, self.frame)

      #add the data
      if "data" in template:
         self.data = template["data"]     
         for k, v in template["data"].items():
             addObject( self.dataFrame, k, template["data"][k], value )

      if "edit" in template:
         editFlag = template["edit"]
      else:
         editFlag = False

      if editFlag is True:
         ButtonNode( "AddObject", "Add Key", self.frame, self.addKeyReqFunction ) 

   ##@brief Callback function for when a new button is pressed
   def addKeyReqFunction( self ):
      AddDialog( self.dataFrame, self.addKeyFunction )

   ##@brief Callback function for when a new button is pressed
   def addKeyFunction( self, data):
      addObject( self.dataFrame, data["key"], data )


##@brief Class for a button node 
class ButtonNode():     
   ##@brief initialization function
   def __init__(self, key, text, parent, callback):
      self.key = key

      frame = tk.Frame(parent)
      frame.pack()
      self.button = tk.Button( frame, text=text, command = lambda: callback())
      self.button.pack()

##@brief class for a text box
class TextBoxNode(BaseObject):
   def __init__( self, parent, key, value, edit = True ):
      self.parent = parent
      self.key = key

      frame = tk.Frame( self.parent)
      frame.pack()
      frame.pack(fill = tk.X)
   
      label = tk.Label( frame, text=key)
      label.pack( side = tk.LEFT)
      self.entry = tk.Entry( frame )
      self.entry.insert(0, value)
      self.entry.pack( expand = True)

      #if we are not editing, disable
      if not edit:
         self.entry.config(state = tk.DISABLED )

   #get the data from the object
   def getData( self ):
      data = {}
      data["key"] = self.entry.get()
      return data


   ##@brief function to update parent (and return data)
   def updateData(self):
      value = self.entry.get()
      self.parent.data[key] = value
      return value


##@brief class for creating TK GUIs on the fly
class tkFactory(BaseObject):
   running = True
   root         = -1
   loopCallback = ""
   loopDuration = 1000

   ##@brief initialize the main window and start the mainloop
   def __init__(self, template, width, height ):
      BaseObject.__init__(self, "root" )
 
      self.window = tk.Tk()
      self.window.title(template["name"])
      self.window.geometry(str(width)+"x"+str(height))
      self.window.data = {}
  
      self.frame = tk.Frame(self.window)
      self.frame.pack()

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
      self.data = {}
      self.name = name
      self.frame.pack()
      self.window.data = addObject( self.frame, self.name, template, value )
