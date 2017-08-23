#!/usr/bin/python3

import json
import tkinter as tk
from tkinter import ttk

##@brief adds a label
def addLabel(labelText, parent, pos=tk.LEFT ):
   frame = tk.Frame( parent)
   label = tk.Label( frame, text=labelText )
   label.pack( side = pos)
   frame.pack()

##@brief Class for a popup window that allows creation of a new dialog
class AddDialog:
    data = {}

    ##@Initialization function
    def __init__(self, parent, callback ):
      #Add callback. 
      self.callback = callback
      self.parent = parent
      self.top = tk.Toplevel(self.parent)
      frame = tk.Frame( self.top )
      frame.pack()

      self.keyTextBox = TextBoxNode( frame, "key", None, self.update, True)

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

      self.descTextBox = TextBoxNode( frame, "Description", None, self.update, True)

      #Creatre a cancel button
      cb = tk.Button(self.top, text="Cancel", command=self.cancel)
      cb.pack(pady=5)

      #Creatre an OK button
      b = tk.Button(self.top, text="OK", command=self.ok)
      b.pack(pady=5)

    def update(self, key, value):

      if value is not None:
         self.data[key] = value

    def cancel(self):
        print("Cancelling")
        self.top.destroy()

    ##@brief accept button callback
    def ok(self):
        output = {}
        value = self.keyTextBox.getData()
        print("OK Value: "+str(value))
        for k in value:
           if value[k] is not None:
               output[k] = value[k]
        
           value = self.descTextBox.getData()
           for k in value:
              if value[k] is not None:
                  output[k] = value[k]
        
        output["type"]     = self.typeField.get()
        output["edit"]     = bool(self.editFlag.get())
        output["required"] = bool(self.requiredFlag.get())
        output["auto"]     = bool(self.autoFlag.get())
       
        self.callback(output)
        self.top.destroy()


##
# @brief    function to add a new object to the GUI. 
#
# @param    parent widget that the generated content will be assigned to
# @param    key the key that the widget represents
# @param    template a dictionary that indicates what kind of data there is
# @param    value to assign to the specified key
# @param    cb callback function to call on change
#
# This function adds an object to the widget pointed to by parent. 
##
def addObject( parent, key, template, value = None, cb = None):
   if "edit" in template:
      editFlag = template["edit"]
   else:
      editFlag = True

   if template["type"] == "dictionary" or template["type"] == "template":
      child = DictionaryNode( parent, template, key, value, cb )
   elif template["type"] == "string":
      if "value" in template:
         value = template["value"]
      else:
         value = ""

      child = TextBoxNode( parent, key, value, cb, editFlag)
      parent.pack()
   else:
      child = None
   
   return child

##@brief base class for extracting data from components
class BaseObject:
   type   = None                    ## @var type of object
   parent = None                    ## @var reference to the parent widget
   key = None                       ## @var key to reference this object
   value = None                     ## @var current value of this object
   cb = None                        ## @var callback for when change occurs
   children = []                    ## @var array of child objects

   ##
   # @brief Initialization function specifies the key
   #
   # @param key Name of the object
   # @param value value of the object
   # @param cb callback function to call on change
   #
   def __init__(self, parent, key, value = None, cb = None):
      self.parent = parent
      self.key = key
      self.cb = cb
      self.value = value

      if value:
         self.value = value

   ##@brief function to update data
   def updateData( self, key, value ):
#      self.data[key] = value
      if self.cb is not None:
         self.cb( self.key, self.value)

   def getData( self ):
      if self.cb:
         self.cb( self.key, self.value )

      data = {}
      data[self.key] = self.value
      return data


##@brief Create a dictionary object
#
# @param parent reference to the parent tk object
# @param key key that will map to the key/value pair
# @param template template object that defines what information should be in the dictionary
# @param value an object that matches the template teh contains the object value(s)
class DictionaryNode(BaseObject):
   data = {}
   def __init__(self, parent, template, key, value = None, cb = None ):

      BaseObject.__init__(self, parent, key, value, cb)

      self.cb = cb
      self.children = []
      
      if value: 
         self.value = value
      else:
         self.value = {}

      self.frame = tk.Frame(parent)
      self.frame.pack( expand = True )


      self.dataFrame = tk.Frame(self.frame)
      self.dataFrame.pack( expand = True )

      #add a label at the top
      addLabel(key, self.dataFrame)

      #add the data
      if "data" in template:
         self.data = template["data"]     
         for k, v in template["data"].items():
             child = addObject( self.dataFrame, k, template["data"][k], value, self.updateData )
             self.children.append(child)

      if "edit" in template:
         editFlag = template["edit"]
      else:
         editFlag = False


      if editFlag is True:
         ButtonNode( "AddObject", "Add Element", self.frame, self.addKeyReqFunction ) 

   ##@brief function to update data
   def updateData( self, newkey, value ):
      self.data[newkey] = value 
      if self.cb:
         self.cb( self.key, self.data)

   def getData( self ):
      for child in self.children:
         item = child.getData()

         if item is not None:
            for k in item:
               self.data[k] = item[k]

      if self.cb:
         self.cb( self.key, self.data)

      result = {} 
      result[self.key] = self.data
      return result


   ##@brief Callback function for when a new button is pressed
   def addKeyReqFunction( self ):
      AddDialog( self.dataFrame, self.addKeyFunction )

   ##@brief Callback function for when a new button is pressed
   def addKeyFunction( self, data):
      child = addObject( self.dataFrame, data["key"], data, self.updateData)
      self.children.append(child)


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
   def __init__( self, parent, key, value, cb, edit = True ):
      BaseObject.__init__(self, parent, key, value, cb)
      self.type = "string"
      self.parent = parent
      self.key = key

      if value:
         self.value = value
      else:
         self.value = ""

      frame = tk.Frame( self.parent)
      frame.pack()
      frame.pack(fill = tk.X)
   
      label = tk.Label( frame, text=key)
      label.pack( side = tk.LEFT)

      sv = tk.StringVar()

      if not value:
        value = ""
      sv.set(str(""))
      sv.trace("w", self.getData)
      self.entry = tk.Entry( frame )
      self.entry.bind("<FocusOut>", self.readData)
      self.entry.bind("<Return>", self.readData)
      self.entry.insert(0, value)
      self.entry.pack( expand = True)
#      self.entry.bind(self.changed)

      #if we are not editing, disable
      if not edit:
         self.entry.config(state = tk.DISABLED )


   #get the data from the object
   def readData( self, update = True):
      value = self.entry.get()
      self.updateData( self.key, value)

   def getData( self ):
      self.value = self.entry.get()
      result = {}
      result[self.key] = self.value 
      return result

      


##@brief class for creating TK GUIs on the fly
class tkFactory(BaseObject):
   running = True
   root         = -1
   loopCallback = ""
   loopDuration = 1000

   ##@brief initialize the main window and start the mainloop
   def __init__(self, template, width, height, cb = None ):
      self.window = tk.Tk()
      self.window.title(template["name"])
      self.window.geometry(str(width)+"x"+str(height))
      self.window.data = {}
      self.children = []
      self.cb = cb

      self.frame = tk.Frame(self.window)
      BaseObject.__init__(self, self.frame, "root", None, cb)
      self.value = {}
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
      addLabel(self.name, self.frame)
#      self.cb = None;

 
      child = addObject( self.frame, "", template, "", self.updateData)
      self.children.append(child)

      ButtonNode( "AddDoc", "Save", self.frame, self.addDocFunction ) 

   ##@brief Callback to insert add document to the database
   def addDocFunction(self):
      result = self.getAllData()

      if self.cb is not None:
         self.cb(self.key,  self.value)


   ##@brief Callback that is triggered when a widget updates
   def updateCallback( self, key, value ):
      self.data[key] = value


   def getAllData( self ):
      for child in self.children:
         item = child.getData()

         if item is not None:
            for k in item:
               self.value[k] = item[k]


      result = {}
      result[self.key] = self.value
      return result

