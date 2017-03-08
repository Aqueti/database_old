//Socket Io interface
"use strict";

var socket = null;


/************************************************************
 * Initialization function that establishes connection when run
 ************************************************************/
var Init; (Init = function Init () 
{
   //Establish socket connection 
//   socket = io.connect('http://spinoza2.disp.duke.edu:');
   socket = io.connect('http://localhost:');
//   socket = io.connect('http://ec2-54-221-146-22.compute-1.amazonaws.com');
})()

var db = 
{
   setSnap: function(args, callback)
   {
      //Establish listen function to process results
      socket.once('added', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(data);
         }
      });

      //Everything is ready. Emit data request. Call back should take results.
      socket.emit("addData", args);
   },

   /************************************************************
   * getCollections object
   ************************************************************/
   getCollectionList: function (args, callback)
   {
      //Set up listener for changing the collection
      socket.once('getCollections', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(data, args);
         }
      });

      //Send request, response triggers listener.
      socket.emit("getCollections","");
   },


   /************************************************************
   * getData object
   *
   * inputs
   ************************************************************/
   getDocuments: function (args, callback)
   {
      
      //Establish listen function to process results
      socket.once('documents', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(data, args);
         }
      });
                
      //Everything is ready. Emit data request. Call back should take results.
      //args should have collection, sort, and query
      socket.emit("getDocuments", {"collection":args["collection"],"query":args["query"],"sort":args["sort"]});
   },


   /************************************************************
   * getData object
   *
   * inputs
   ************************************************************/
   getData: function (args, callback)
   {
      //Establish listen function to process results
      socket.once('data', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            args["data"] = data;
            callback(args);
         }
      });
                
      //Everything is ready. Emit data request. Call back should take results.
      //args should have collection, sort, and query
      socket.emit("getData", {"collection":args["collection"],"query":args["query"],"sort":args["sort"]});
   },

   /************************************************************
    * loadTemplate
    *
    * Generate a dropdown list for an dictionary passed in
    *
    * Inputs:
    *    args[url] - link to the file to load
    *    callback  - callback function to process loaded data
    ************************************************************/
   getTemplates: function(args, callback)
   {
      var request = {}
      request.collection = "templates"
      request.query = {"collection":args["collection"]}

      //Establish listen function to process results
      socket.once('getTemplates', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(data,args)
         }
      });

      //Everything is ready. Emit data request. Call back should take results.
      socket.emit("getTemplates", request);
   },

   /************************************************************
    * getQueryTemplate
    *
    * Generate a dropdown list for an dictionary passed in
    *
    * Inputs:
    *    args[url] - link to the file to load
    *    callback  - callback function to process loaded data
    ************************************************************
   getQueryTemplate: function(args, callback)
   {
      //Establish listen function to process results
      socket.once('getTemplates', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(args, data)
         }
      });
                    
      var request = {};
      request["collection"] = args.collection;
      request["type"] = "query";

      //Everything is ready. Emit data request. Call back should take results.
      socket.emit("getTemplates", request);
   },
*/
   /************************************************************
   * genNewId - function to get a new id
   *
   * inputs
   ************************************************************/
   genNewId: function (args, callback)
   {
      //Establish listen function to process results
      socket.once('newId', function(data)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            args.id=data;
            args.query ={"id":data};
            callback(args);
         }
      });
                
      //Everything is ready. Emit data request. Call back should take results.
      //args should have collection, sort, and query
      socket.emit("getNewId", args);
    },

   /************************************************************
   * setData object
   *
   * inputs
   ************************************************************/
   setData: function (data, callback)
   {
      if( !isObject(data["query"]))
         data["query"]={};
      if( !isObject(data["sort"]))
         data["sort"]={};
                                 
      //Establish listen function to process results
      socket.once('set', function(result)
      {
         if(data.error)
         {
            alert("Data transmission error!");
         }
         else
         {
            callback(data);
         }
      });

      //Everything is ready. Emit data request. Call back should take results.
      socket.emit("setData", data);
    }
   
};

