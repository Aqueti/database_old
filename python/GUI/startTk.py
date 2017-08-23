#!/usr/bin/python3
import sys
import os
sys.path.append("..")

from AJSON import readJson
import argparse
import tkFactory

##@brief callback for mainloop
def windowCallback():
   pass

##@brief Callback to be notified of a change
def updateCallback( key, value ):
   print("Factory Ouput for "+key+": "+str(value))

##@brief Main function
def main():
   template = {"name":"test", "type":"string"}

   # parse command line arguments
   parser = argparse.ArgumentParser(description='AWARE Database Script')

   parser.add_argument('-c', action='store', dest='config',   help='config file to use')
   parser.add_argument('-t', action='store', dest='template', help='template file to use')

   #Parse arguments
   args = parser.parse_args()

   if args.config:
      data = readJson( args.config );

   if args.template:
      template = readJson( args.template)

   #Create GUI
   window = tkFactory.tkFactory( template, 500, 500, updateCallback)
   window.generate( "Test TK", template )
   window.start(windowCallback, 1000)
     

if __name__ == "__main__":
   main()
