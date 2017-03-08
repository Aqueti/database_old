#!/usr/bin/python
"""
############################################################
# AWS.py - Amazon web-services interface. 
#
# This class provides a consistent interface to Amazone web
# services components. 
#
# Developed by: Steve Feller
# Date: 2/9/2014 - Created
############################################################
"""
import os
import argparse
import boto
from boto.s3.connection import S3Connection


class AWS:
   """Interface to a MongoDB Database."""  
   
   #class variables
   connection=""

   #############################################
   # Initialization function 
   #
   # Inputs:
   #   access - access key
   #   secrt  - secret key
   #
   # Returns:
   #  -1 - Unable to establish link
   #   1 - OK
   # 
   # Notes: 
   #   - needs additional error checking
   ############################################
   def __init__(self):
      #set default verbosity level
      self.Verbose =0


   #############################################
   # connect
   #
   # Inputs:
   #   level - verbosity level to use for debugguing
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def connect( self, access, secret ):

      #Connect to AWS
      if self.Verbose > 1:
         print "Connecting to S3 with "+access+":"+secret
      try:
         self.connection = S3Connection(access, secret);
      except:
         print "Unable to establish a connection. Failed on Init"
         return -1

      print "Connected to AWS"
      return 1

   #############################################
   # setVerbose
   #
   # Inputs:
   #   level - verbosity level to use for debugguing
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def setVerbose( self, level ):
      if level > 0:
         print "AWS::setVerbose: setting verbose level to "+str(level)
      self.Verbose = level
      
   #############################################
   # CreateBucket
   #
   # Inputs:
   #   data - dictionary to be inserted in database 
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def createBucket(self, name):
      """Add a bucket ot the database"""
      
      try:
         self.conn.create_bucket(name)
      except:
         print "Unable to create bucket. It may already exist"

      print "Bucket "+name + "created"
      return 1;

   #############################################
   # getBuckets
   #
   # Inputs:
   #    none
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def getBuckets(self):
      try:
         buckets = self.connection.get_all_buckets()
      except:
         print "Unable to get all buckets in connection"
         return None

      return buckets

   #############################################
   # List Buckets
   #
   # Inputs:
   #    none
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def listBuckets(self):
      buckets = self.getBuckets();
      for key in buckets:
         print key.name.encode('utf-8')

      return 

   #############################################
   # getObjectList
   #
   # Inputs:
   #    none
   #
   # Returns:
   #   -1 - Unable to get object list for bucket
   # list - list of all objects in bucket
   #############################################
   def getObjectList(self, bucket ):
      if self.Verbose > 0:
         print "AWS::getObjectList: Showing objects for bucket "+bucket

      #Get bucket from S3
      try:
         objects = self.connection.get_bucket(bucket)
      except:
         print "Unable to get object in bucket: "+bucket
         return None

      return objects

   #############################################
   # List Objects
   #
   # Inputs:
   #    none
   #
   # Returns:
   #   rc - number of inserted documents
   #############################################
   def listObjects(self, bucket ):
      if self.Verbose > 0:
         print "AWS::listObjects: Showing objects for bucket "+bucket

      objects = self.getObjectList(bucket)

      for key in objects.list():
         print key.name.encode('utf-8')

      return 1

   #############################################
   # getJson
   #
   # Inputs:
   #   key       - object key to download
   #
   # Returns:
   #   dict - object values.
   #     -1 - unable to get bucket
   #     -2 - unable to get key
   #     -3 - unable to download file
   #############################################
   def getJson( self, key):
      if self.Verbose > 0:
         print "AWS::getJSON: Showing objects for key "+str(key)

      return key.get_contents_as_string()

      #Connect to bucket
      try:
         bucket = conn.get_bucket(buck_name)
      except:
         if self.Verbose > 1:
            print "AWS::getJSON: Unable to open bucket: "+buck_name
         return -1

      #get key name from the bucket and then get 
      try:
         key = bucket.get_key(key_name)
      except:
         if self.Verbose > 1:
            print "AWS::getObject: Unable to get key: "+key_name
         return -2
 
      try:
         data=key.get_contents_as_string()
      except:
         if self.Verbose > 1:
            print "AWS::getJSON: Unable to read key: "+key_name
         return -3
 
      #Convert string into dictionary
      return eval(data);


"""
############################################################
#      bucket = conn.get_bucket('aqueti.data')
#      for key in bucket.list():
#         print key.name.encode('utf-8')

# Main()
#
# Main function for testing. Interface for command line as
# well as python shell
#
# Notes:
#    - This 
############################################################
"""
def main():
   """ Main function for testing the class """
   VERBOSE = 0

   parser = argparse.ArgumentParser(description="AWS S3 storage interface")

   parser.add_argument('-v', action='store_const', dest='VERBOSE', const='True', help='VERBOSE output')
   parser.add_argument('-vv', action='store_const', dest='VERBOSE2', const='True', help='VERBOSE output')
   parser.add_argument('-a', action='store', dest='aws_access', help='AWS Access Key')
   parser.add_argument('-secret', action='store', dest='aws_secret', help='AWS Secret Key')
   parser.add_argument('-l', action='store_const', dest='list_objects', const='True',  help='List all objects from the URL')
   parser.add_argument('-p', action='store', dest='put', help='add specified file into dictionary')
   parser.add_argument('-g', action='store', dest='get', help='Get option')
   parser.add_argument('bucket', help='Name of bucket to work with (ALL = all buckets)')

   args=parser.parse_args()

   #set verbosity leve
   #Establish S3 connectionsl
   if args.VERBOSE:
      VERBOSE = 1

   if args.VERBOSE2:
      VERBOSE = 2

   #Create AWS class
   aws=AWS()
   aws.setVerbose( VERBOSE );

   #Connect AES service
   print "Connecting to AWS: "+args.aws_access+","+args.aws_secret
   aws.connect( args.aws_access, args.aws_secret)

   #Use command line data to set host and port
   #sdf - needs to be checked
   #if args.host != "" and args.port != -1:
   #   mdb = MDB(args.dbase, args.host, args.port)
   #else:
   #   mdb = MDB(args.dbase)
   if args.list_objects:
      if args.bucket == "ALL":
         aws.listBuckets()
      else:
         aws.listObjects( args.bucket )


"""
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

   if args.list:
     if VERBOSE > 0:
        print "Listing files"

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
if __name__ == "__main__":
#   sys.exit(main())
   main()


