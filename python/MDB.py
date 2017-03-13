#!/usr/bin/python

##@package MDB.py
# @brief General mongodb database interface in python.
# @author Aqueti, Inc.
# @date 12/27/12
# 
# This package contains the MDB class that provides a low-level interface
# to a mongodb server as well as a command line interface for access
# database information from the system
#

import sys
import argparse
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

import json
import AJSON

## @class MDB
# @brief class that maintains a persistent connection to a mongo dabase.
#
# The MDB class is designed to persist during database access. It contains the
# low-level functionality to interact with a mongodb database.
##
class MDB:
   """Interface to a MongoDB Database."""  
   
   connection = ""                         # connection information
   db = ""                                 # var database name

   ##
   # @brief Initialization function
   # This function is called when the class is created. It sets
   # class variables to their defaults
   ##
   def __init__(self ):
      print "Initialize MDB"

   ##
   # @brief Connects to the specified datbase
   # @param dbase name of the database to connect to
   # @param host hostname of the mongoDB server
   # @param port port of the mongod instance on the server
   # @return None
   #
   # This function is used to connect to a database. If no host
   # or port is specified, it will default to localhost at the
   # default MongoClient port by default.
   ##
   def connect(self, dbase, host='none', port='none' ):
      """Intialization Function"""
      print "Initializing: "+dbase
      
      #establish connection 
      if host != 'none' and port != 'none':
         self.connection = MongoClient(host,port)
      else:
         self.connection = MongoClient()

      #link database
      self.db = self.connection[str(dbase)]

  

      return

   ## 
   # @brief Inserts the document indicated by data into the specified collection
   #
   # @param collection name of the collection to inser thte document into
   # @param document document to insert
   # @param force flag to insert the document without template verification
   # @return -1 on failure, 1 on success
   #
   # This function is used pushes the specified document into the database. By default
   # it the database for a template file that is based on the collection name
   # and templateVersion field within the document if provided and ensures that the new 
   # document matches the template requirements. If the force variable is set to true, 
   # the new document is added to the database without verification.
   ##
   def insert(self, collection, document, force):
      """Insert a document into the database """
      templateQuery = {}
      templateQuery["name"] = collection


      #if force, insert the document without any checks and return
      if force:
         try:
            print "Force Inserting: "+str(document)
            self.db[collection].insert(document)
            return 1
         except:
            e = sys.exc_info()[0]
            print "Error on forced inserting:"+str(e)
            return -1

      #Get template for comparision. If the document specifies a template, u
      if document["template"]:
         templateQuery["name"] = document["template"]

      if document["templateVersion"]:
         templateQuery["version"] = document["templateVersion"]

      #get a list of templates and select the last (by date)
      templateList = self.query( "templates", templateQuery )
      count = len(templateList)
      if count < 1:
         print "No template found"
         return -1
     
      if count > 1:
         print str(count)+" template found. Using most recent"
         
  
      #get the last template in the list
      templateList = sorted( templateList, key=lambda k: k["date"])
      template = templateList[count -1]

      #Verify template
      result = self.validate( document, template )

      if result :
         #make sure the record doesn't already exist
         query = {}
         key = template["key"]
         query[key]= document[key]

         #query the collection. 
         records = self.query(collection, query )
         if len(records) > 0 :
            print len(records)+" matching items found. Not inserting."
            return -1

         #finally insert the document
         try :
            self.db[collection].insertOne( document );
         except:
            e = sys.exc_info()[0]
            print "Error: "+ str(e)
            return -1;
      return 1

   #############################################
   # Update Document 
   #
   # Inputs:
   #   data - dictionary to be inserted in database 
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def update(self, collection, data):
      """Insert a document into the database """

      #specify collection
      coll = self.db[collection]

      try :
   
         coll.update(data)
      except:
         e = sys.exc_info()[0]
         print "Error: "+ str(e)

   #############################################
   # Query Document
   #
   # Inputs: 
   #   coll - collection to query
   #   data - {key:value} dictionary to search for
   #   action - option on data process
   #      'count' - returns number of elements found
   #   'sort = key'  - sorts the results by given key
   #
   # Returns:
   #   result - list of returned values
   #############################################
   def query(self, coll, data, action='none', sort='none'):
      """ Query a document from the database """
      posts = self.db[coll]

      print "MDBQuery: "+str(coll)+", "+str(data)

      results = posts.find(data)

      #count strings
      if action == 'count':
         return len(results)

      #find all matching posts
      result = []

      if sort == 'none':
         for post in results:
            result.append(post)
      else:
         print "Sorting: "+sort
         for post in results.sort(sort):
            result.append(post)

      return result

   #############################################
   # Get a list of collections
   #############################################
   def getCollections(self):
      return self.db.collection_names()
   
   #############################################
   # Dump Database
   #############################################
   def dump(self, action='none'):
      """Get all documents in a database """
      posts = self.db.posts

      #count strings
      if action == 'count':
         return posts.count()

      #return list
      result = []
      for post in posts.find():
         result.append(post)

      return result

"""
############################################################
# Main()
#
# Main function for testing. Interface for command line as
# well as python shell
############################################################
"""
def main():
   """ Main function for testing the class """
   VERBOSE = 0
   host=""
   port=-1

   parser = argparse.ArgumentParser(description="MDB AWARE Datbase interface")

   parser.add_argument('-v', action='store_const', dest='VERBOSE', const='True', help='VERBOSE output')
   parser.add_argument('-vv', action='store_const', dest='VERBOSE2', const='True', help='VERBOSE output')
   parser.add_argument('-a', action='store', dest='add', help='add specified file into dictionary')
   parser.add_argument('-c', action='store_const', dest='collection', const='True', help='query speficied key pair')
   parser.add_argument('-p', action='store', dest='port', help='port of the mongodb server')
   parser.add_argument('-s', action='store', dest='host', help='hostname of mongodb server')
   parser.add_argument('-q', action='store', dest='query', help='query speficied key pair')
   parser.add_argument('-d', action='store_const', dest='dump', const='True', help='query speficied key pair')
   parser.add_argument('-list-collections', action='store_const', dest='listCollections', const='True', help='query speficied key pair')
   parser.add_argument('-o', action='store', dest='outfile', help='output file')
   parser.add_argument('dbase', help='database to reference')

   args=parser.parse_args()

   #set verbosity level
   if args.VERBOSE:
      VERBOSE = 1

   if args.VERBOSE2:
      VERBOSE = 2

   #Use command line data to set host and port
   mdb = MDB();
   if args.host  and args.port :
      mdb.connect(args.dbase, args.host, args.port)
   else:
      mdb.connect(args.dbase)

   if VERBOSE > 0:
     print "Using "+args.dbase+" as the database"

   #if -c option list collections
   if args.listCollections:
      AJSON.printJson(mdb.getCollections())

   #add specified file to the database
   if args.add:
  
      if VERBOSE > 0:
         print "Reading :"+args.add

      #load JSON file
      data = AJSON.readJson(args.add)
 
      print "Should add data here"
      mdb.insert(collection,data)

   #query database
   if args.query:
      if VERBOSE > 0:
         print "Query: "+args.query
 
      mdb.query(args.query)

   #dump database
   if args.dump:
      if VERBOSE > 0:
         print "Dumping..."

      if args.action:
         rc = mdb.dump(action=args.action)
         print "Count: "+str(rc)

      else:
         rc = mdb.dump()

         for item in rc:
            print str(item)+"\n"

 

"""
############################################################
# Map __main__ to main()
############################################################
"""
if __name__ == "__main__":
   sys.exit(main())



