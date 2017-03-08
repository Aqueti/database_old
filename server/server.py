#!/usr/bin/python
"""
# ADB.py
#
# Functions to manage the Aqeuti database interface
#
# This file is used to merge a heirarchy of json files used to track AWARE 
# Imaging System.
#
# Created by: Steve Feller on 11/8/2012
# Release Date:
#
# Modified:
#    1/22/2014 - Steve Feller - Added file system interface support
#    2/9/2014  - Steve Feller - Added support for AWS
# versions: 0.2
#
# Functions:
#    generate(path)  - function to generate a dictionary of 
#                      the json data using the given path as
#                      the root.
#    writeDict(dest) - function to write the current dictionary
#                      to the specified file
#    query(key)      - function to get a list of all values for the given key
#    findKeys(value) - function to find a key that matches a given value
#
#    genDict(path)   - recursive function that step through
#                      subdirectories of the given path and 
#                      aggregates data into a single dictionary
#                      that is returned. 
#
#                       Any data that needs to be adjusted in handled within
#                     this function.
#
#    findKeys - recursive function to find keys for a given value
#    stringList(dbase) - iterative generate a list of strings for each value
#                     for each value in a dictionary. 
#
# Proposed functions:
#   writeDB - exports current dictionary to the the JSON file heirarchy
#
# Notes:
#   - need to add wildcard support to lookup functions (query, findkeys)
############################################################
"""
import os
import argparse
import json
import datetime
import time
import subprocess

from socketio.server import SocketIOServer
from socketio import socketio_manage
#from pyramid.paster import get_app
from gevent import monkey; monkey.patch_all()
import base64
from socketio.namespace import BaseNamespace

from subprocess import call

#custom files
import AJSON                                #JSON file interface functions
import MDB                                  #mongodb database interface class
#import AWS                                  #amazon web services interface

VERBOSE = 1;
mdb = None;
#collections = ["composites","albums","snapshots"]
collections = []
port=8088

############################################################
# SocketIO Class
############################################################
class AquetiNamespace(BaseNamespace):
   global mdb

   _registry = {}

   def initialize(self):
      self._registry[id(self)] = self
      self.emit('connect')
      self.nick = None

   def disconnect(self, *args, **kwargs):
      if self.nick:
         self._users.pop(self._nick, None)
      super(AquetiNamespace, self).disconnect(*args, **kwargs)

   def on_login(self, nick):
      if self.nick:
         self._broadcast('exit', self.nick)
      self.nick = nick
      self._broadcast('enter', nick)
      self.emit('users',
                [ ns.nick
                  for ns in self._registry.values()
                  if ns.nick is not None ])

   def on_chat(self, message):
      if self.nick:
         self._broadcast('chat', dict(u=self.nick, m=message))
      else:
         self.emit('chat', dict(u='SYSTEM', m='You must first login'))

   def _broadcast(self, event, message):
      for s in self._registry.values():
         s.emit(event, message)

   #get a list of documents for hte given collection (and query)
   def on_getDocuments( self, data ):
      #see if we have a template
      print "getting documents: "+str(data);
#      try:
#         data.templates = mdb.query("templates", {"collection":data["collection"]})
#      except:
#         print "Template does not exist for collection named "+data["collection"]

      docs = mdb.query( data["collection"], data["query"] );

      data = convertIdToString(docs)

      print("Results: "+str(data))
      self.emit("documents", data)

      


   #requests a list of collections
   def on_getCollections(self,data):
      print "Getting collections"
      collections = mdb.getCollections()
      self.emit('getCollections',collections)

   #############################################
   # add data
   #############################################
   def on_setData(self, data):
      mdb.insert(data["collection"], data);
      self.emit('set',"ok");

   #############################################
   # add data for snapshot
   #############################################
   def on_addData(self,data):
      if "id" not in data:
         data["id"] = str(int(time.time()))

      msg = {}
      msg["data"] = data
      msg["collection"] = "snapshots"
      msg["query"] = {"id":data["id"]}
      msg["sort"] = {}

      #insert mesg
      mdb.insert(msg["collection"], msg)

      self.emit('added',{"id":data["id"]})

   ##############################
   # generate a new ID
   ##############################
   def on_getNewId(self, data):
      t = int(time.time())
      self.emit('newId',t)

   ##############################
   #get data from the database
   ##############################
   def on_getData(self, data):
      print str(data);
      result = mdb.query( data["collection"], data["query"])

      #remove the internal _id values
      result = remove_Id(result)

      print
      print "get Data result: "+str(result)
      print

      #if we're an albums, fill out items data
      if data["collection"] == "albums":

         #loop through each album
         for i in range(len(result)):
            items = result[i]["items"]
 
            #get data for each item/document in the album
            for j in range(len(items)):
               q = {"id":items[j]["id"]}

               key = str(items[j]["doctype"])
               key = key+"s";
               res = mdb.query( key, q) 
               res = remove_Id(res)

               try:
                  items2 = res[0]["items"]
                  for k in range(len(items2)):
                     q = {"id":items2[k]["id"]}

                     key2 = str(items2[k]["doctype"])
                     key2 = key2+"s";
                     res2 = mdb.query( key2, q) 
                     res2 = remove_Id(res2)
                     items2[k]["data"] = res2[0]
                  
                  res[0]["items"] = items2
               except:
                  pass

               print
               print str(res)
               print


               try:
                  items[j]["data"] = res[0]
               except:
                  pass


            result[i]["items"] = items;

      print "Complete! : "+str(result)

      #return result
      self.emit("data",result)

   ##############################
   # getTemplates
   ##############################
   def on_getTemplates(self, data):
       print "Template request:" + str(data)
#      template = AJSON.readJson(data["type"]+".json")
#      print("Template:"+str(template))
#      print("Template: "+str(data["type"])+".json")
#      self.emit("template", template["collections"][data["collection"]]["data"])

       templates = mdb.query( "templates", data["query"] )
   
       #Strip the interneral id files
       for i in range(len(templates)):
         try:
            templates[i]["_id"] = str(templates[i]["_id"])
         except:
            print "ObjectId not found at index"+str(i)
   
       self.emit("getTemplates", templates)
    

   ##############################
   # sendFile
   ##############################
   def on_sendFile( self,data):
      print "received image"
     
#     data = base64.b64decode(data_in);

      files =["tif","jpg","jpeg","JPG","TIF","tiff"]

      if( data["ext"] not in files):
         self.emit("recieved","invalid type")
         print "Invalid type"+str(data["ext"])
         return

      #get date for filename
      if data["start"] == True:
         t = int(time.time())
      else:
         t = data["name"];

      fname = "composites/"+str(t)+"."+data["ext"]

      print "Saving as: "+fname
      
      #download data as file with timestamp and given type
      #if starting, open file wb
      if data["start"] == True:
         with open(fname,'wb') as f:
            f.write(base64.b64decode(data["data"]))
      #if appending, open ab
      else:
         with open(fname,'ab') as f:
            f.write(base64.b64decode(data["data"]))

      result = {};
      result["name"] = str(t)
      result["done"] = False

      #if end, then process image
      if data["end"] == True:
         #run compositing/s3 upload script
         subprocess.call(['./processImage.sh', fname])
         result["url"] = "http://s3.amazonaws.com/aqueti.data/composites/"+str(t)+"/"+str(t)+".tiles/index.html"
         result["done"] = True;

         self.emit("received", result)
      else:
         self.emit("received", result);

def chat(environ, start_response):
    if environ['PATH_INFO'].startswith('/socket.io'):
#       return socketio_manage(environ, { '/chat': AquetiNamespace })
       socketio_manage(environ, {'': AquetiNamespace})

    else:
       return serve_file(environ, start_response)

def serve_file(environ, start_response):
   public = "/home/sfeller/develop/aware/server2/web"
   print "Path:"+str(public)
   path = os.path.normpath( os.path.join(public, environ['PATH_INFO'].lstrip('/')))
   assert path.startswith(public), path
   if os.path.exists(path):
        start_response('200 OK', [('Content-Type', 'text/html')])
        with open(path) as fp:
            while True:
                chunk = fp.read(4096)
                if not chunk: break
                yield chunk
   else:
        start_response('404 NOT FOUND', [])
        yield 'File not found'


############################################################
# remove_Id
############################################################
def convertIdToString(data):
   print( str(data))
   for item in data:
      try:
         item["_id"] = str(item["_id"])
      except: 
         print "_id not found: "+str(item)

   return data

"""
############################################################
# Main function
############################################################
"""
def main(): 
   global VERBOSE
   global mdb 
   global collection
   global port

   #default access info
   awsAccessKey = 'AKIAJICPBE3SSHW5SR7A'
   awsSecretKey = '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'
   awsBucket    = 'aqueti.data'
  
   #parse inputs
   # parse command line arguments
   parser = argparse.ArgumentParser(description='Python server')

   parser.add_argument('-v', action='store_const', dest='VERBOSE', const='True', help='VERBOSE output')
   parser.add_argument('-vv', action='store_const', dest='VERBOSE2', const='True', help='VERBOSE output')
   parser.add_argument('-a', action='store', dest='aws_access', help='AWS access code')
   parser.add_argument('-s', action='store', dest='aws_secret', help='path to data')
   parser.add_argument('-b', action='store', dest='bucket', help='S3 Bucket with data')

   """
   parser.add_argument('-p', action='store_const', dest='printout', const='True', help='print contents of JSON file')
   parser.add_argument('-d', action='store', dest='path', help='path to data')
   parser.add_argument('-u', action='store_const', dest='update', const='True', help='update records')
   parser.add_argument('-c', action='store', dest='collection', help='collection (table) to use')
   """
   parser.add_argument('dbase', help='database name')

   args=parser.parse_args()

   #set VERBOSE flag as requested
   if args.VERBOSE:
      VERBOSE=1
  
   if args.VERBOSE2:
      VERBOSE=2
      print "VERBOSE=2"

   #extract relevant parameters
   if VERBOSE > 1:
      print "Using database "+args.dbase


   ##################################################
   # connect to database and AWS server (if needed)
   ##################################################
   #connect to database
   mdb=MDB.MDB()
   if VERBOSE > 1:
      print "Connecting to mongodb: "+args.dbase
   try:
      rc = mdb.connect(args.dbase)
   except:
      print "MDB: Unable to connect to database: "+args.dbase
      return -1

#   if args.aws_access:
#      awsAccessKey = args.aws_access

#   if args.aws_secret:
#      awsSecretKey = arts.aws_secret

#   if args.bucket:
#      awsBucket = args.bucket

   # Connect to AWS class
   #sdf - need to make this optional
#   aws=AWS.AWS()
#   aws.setVerbose( VERBOSE );

#   if VERBOSE > 1:
#      print "Connecting to AWS: "+awsAccessKey+"/"+awsSecretKey
#   try:
#      aws.connect( awsAccessKey, awsSecretKey )
#   except:
#      print "Unable to connect to AWS. Please check inputs"
#      return -1

   print "Starting the server on port "+str(port)+"!"
   sio_server = SocketIOServer(
      ('', port ), chat, 
      policy_server=False)
   sio_server.serve_forever()


   #We should be connected ot the database and S3
#   app = get_app('development.ini')
#   print 'Listening on port http://127.0.0.1:8080 and on port 843 (flash policy server)'
#   SocketIOServer(('127.0.0.1', 8080), app, policy_server=False, transports=['websocket']).serve_forever()
"""
############################################################
#Function to validate peformance
############################################################
"""
if __name__ == '__main__':
  main()

