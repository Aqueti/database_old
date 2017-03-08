/*************************************************************
 * aqueti.js
 *
 * Public interface function for aqueti iamges. This suite of 
 * functions allows users to selec the images they are interested in
 *************************************************************/
"use strict";

var ai = null;
var timeOut = null;
var scroll = 0;


/************************************************************
 * Listener function for page events
 ************************************************************/
$(function()
{
   //snapButton button callback
   $("body").on('click', "#snapButton", function()
   {
      var mainDiv = document.getElementById("mainDiv");
      var snapDiv = generateSnapDiv();
      mainDiv.appendChild(snapDiv);
   });

   //snapSubmit button callback
   $("body").on('click', "#snapSubmit", function()
   {
      processSnapshot();
   });

   //queryButton button callback
   $("body").on('click', "#querySubmit", function()
   {
      var queryList = document.getElementById("queryList")
      var query = parseInputTree(queryList);

      //If the query is not valid, 
      if( !utils.isObject(query))
         query = {};

      //Get data with query callback
      var args = {};
      args.query = query;
      args.collection = queryList.getAttribute("title");;
      args.sort={};
      db.getData( args, aqQueryCallback); 
   });

   //snapButton button callback
   $("body").on('click', "#snapCancel", function()
   {
      //Make the snapdiv invisible 
      $("#snapDiv").remove();
   });

   //infoButton button callback
   $("body").on('click', "#infoButton", function()
   {
      $("#infoDiv").toggle();
   });
});


/************************************************************
 * parseInputTree
 *
 * Funcion to extract data from long list
 ************************************************************/
function parseInputTree( root )
{
   var tag = $(root).prop("tagName");
   var children = root.childNodes;
   var title = $(root).attr("title");

   //If UL
   if( tag == "UL")
   { 

      /////////////////////////////////////////////
      //If we're an array
      /////////////////////////////////////////////
      if( $(root).attr("class") == "array")
      {
         var  arr = [];

         for( var i= 0; i <children.length; i++)
         {
            var data = {};

            var tag = $(children[i]).prop("tagName");
            if( tag == "LI")
            {
               
               var local = {};
               var element = parseInputTree(children[i]);

               if(( element != "")&&(element != -1))
                  arr.push(element);
            }
         }

         var data = {};

         if( arr.length ==  0)
            return -1;


         data[title] = arr;

         return data;
      }
      /////////////////////////////////////////////
      //If we're a group
      /////////////////////////////////////////////
      else if( $(root).attr("class") == "group")
      {
         var result = [];
         var data = {};
         for(var i = 0; i< children.length; i++)
         {
            var element = parseInputTree(children[i]);

            if(element != -1)
            {
               var keys = Object.keys(element);
               for( key in keys)
                  data[keys[key]] = element[keys[key]];
            }
         }

         result.push(data);
         return data;
      }

      //Standard list processing
      else
      {
         var result={};
         var data={};

//         var listkey = $(root).attr("title");
         var listkey = title;

         for( var i= 0; i <children.length; i++)
         {
            var value = parseInputTree( children[i]);

            if( value != -1)
            {
               var keys = Object.keys(value);
               for( key in keys)
                  data[keys[key]] = value[keys[key]];
            }
         }


         if( Object.keys(data).length > 0)
            result[listkey] = data;

         var rlen =Object.keys(result).length;
         var dlen =Object.keys(data).length;

         if( Object.keys(result).length == 0)
            return -1;

         return result;
//         return data;
      }
   }
   //If an li element, add to dictionary
   else if( tag == "LI" )
   {
      for( var i = 0; i < children.length; i++)
      {

         var element = parseInputTree( children[i]);
         if(element == -1)
            return element;

         if(isObject(element))
         {
            if(element.length == 0)
               return -1;
         }

         if( element != -1)
         {
            return element;
         }
      }
      return -1;
   }
   //If an input element, return value
   else if( tag == "INPUT")
   {
      var test = $(root).attr("key");
      if(test == "true")
         return -1;

      var data = {};
      var key = title;
      data[key] = $(root).val();

      //If the value is undefined, remove from object
      if(( data[key] == "undefined")|| (data[key] == ""))
      {
         delete data[key];
         return -1;
      }

      return data
   }
   else if( tag == "SELECT")
   {
      var test = $(root).attr("key");
      if( test == "true")
         return -1;

      var data = {};
      var key = title;
//      var s = $(root).find('option:selected');
//      alert("Options:"+s.text());

      data[key] = $(root).find("option:selected").text();
      return data;
   }

   return -1;
}


/************************************************************
 * generateSnapDiv
 *
 * Code to extract position and request text for a snapshot
 ************************************************************/
function generateSnapDiv(args)
{
   //If args is not an object, make it an empty one
   if( ! utils.isObject(args))
      args = {"edit":true};

   //Create snapview
   var snapDiv = document.createElement("div");
   snapDiv.setAttribute("id","snapDiv");

   //Add title
   var h2 = document.createElement("h2");
   snapDiv.appendChild(h2);
   h2.innerHTML = "Snapshot";

   //Add header data
   var title = document.createElement("text");
   var description = document.createElement("text");
   var keywords = document.createElement("text");
   title.innerHTML = "Title:";
   description.innerHTML ="<br>Description:";
   keywords.innerHTML = "<br>Keywords:";
   
   //SnapView title field
   var snapTitle = document.createElement("input");
   snapTitle.setAttribute("type","title");
   snapTitle.setAttribute("title","title");
   snapTitle.setAttribute("id","snapTitle");
   if( "title" in args)
      snapTitle.setAttribute("value",args["title"]);
   snapDiv.appendChild(title);
   if( !args.edit )
      snapTitle.setAttribute("readonly",true);
   snapDiv.appendChild(snapTitle);

   //SnapView description field
   var snapDesc = document.createElement("textarea")
   snapDesc.setAttribute("rows","4");
   snapDesc.setAttribute("cols","32");
   snapDesc.setAttribute("id","snapDesc");
   if( "desc" in args)
      snapDesc.value = args["desc"];
   if( !args.edit )
      snapDesc.setAttribute("readonly",true);
   snapDiv.appendChild(description);
   snapDiv.appendChild(snapDesc);

   //SnapView keywords field
   var snapKeys = document.createElement("input");
   snapKeys.setAttribute("type","text");
   snapKeys.setAttribute("id","snapKeys");
   snapKeys.setAttribute("size","40");
   if( "keywords" in args)
      snapKeys.setAttribute("value",args["keywords"]);
   if( !args.edit )
      snapKeys.setAttribute("readonly",true);
   snapDiv.appendChild(keywords);
   snapDiv.appendChild(snapKeys);

   //Add cancel button
   var cancelButton = document.createElement("button");
   var text = document.createTextNode("Close");
   cancelButton.appendChild(text);
   cancelButton.setAttribute("id","snapCancel");
   snapDiv.appendChild(cancelButton);

   if( args.edit == true)
   {
      //Add submit button
      var subButton = document.createElement("button");
      var text = document.createTextNode("submit");
      subButton.appendChild(text);
      subButton.setAttribute("id","snapSubmit");
      snapDiv.appendChild(subButton);
   
      cancelButton.innterHTML = "Cancel";

   }
   return snapDiv;
}

/************************************************************
 * processSnapshot
 *
 * function that is called when a snap is submitted
 ************************************************************/
function processSnapshot()
{
   var args={};

   //Get position
   args.imageId = $("#mainDiv").attr("imageId");
   args.view = ai.getView();
   args.title = $("#snapTitle").val();
   args.desc = $("#snapDesc").val();
   args.keywords = $("#snapKeys").val();

   db.setSnap( args, snapComplete);
}

/************************************************************
 * snapComplete
 *
 * function that is called when a snap completes upload
 ************************************************************/
function snapComplete(args)
{
   alert("Snapshot saved with id: "+args["id"]);

   //Make snapDiv invisible again
   $("#snapDiv").remove();
}

/************************************************************
 * function to get a list of images
 *
 * This function gets a list of images from the database
 ************************************************************/
function genView()
{
   var action = null;                       //what we do
   var args = {};
   args.collection = "albums";              //By default we generate view by albums
   args.query = {};
   args.sort = {};

   //Convert URL values into input parameters
   var inputParams=utils.getUrlValues();

   //loop through inputs to set up query
   var ids = 0;
   for( var key in inputParams )
   {
      if(( key == "albums")||(key == "composites")|(key == "snapshots"))
      {
         args.collection = key;

         if( inputParams[key] == "query")
         {
            action="query";
         }
         else 
         {
            args.query["id"] = inputParams[key];
         }
      }

      //All all other key/value pairs
      else
      {
         args[key] = inputParams[key];
      }
   }

   var query = {};
   var sort ={};

   //If we're a query, work here.
   if( action == "query")
   {
      //get template for teh specified type
      db.getQueryTemplate(args,genQueryForm);

      return;
   }

   //Select processing loop based on a selection
   if( args.collection == "composites")
      db.getData(args, aqCompositeCallback );
   else if( args.collection == "albums")
      db.getData(args, aqAlbumCallback );
   else if( args.collection == "snapshots")
      db.getData(args, aqSnapCallback);
   else
      alert(args.collection+" is not supported now");
};


/************************************************************
 * Generate a query form from a template
 ************************************************************/
var genQueryForm = function(args, template)
{
   var ul = genUL(template);
   ul.setAttribute("id","queryList");
   ul.setAttribute("title",args.collection);

   //Add a querymit buttons
   var queryButton = document.createElement("button");
   var text = document.createTextNode("Submit");
   queryButton.appendChild(text);
   queryButton.setAttribute("id","querySubmit");
   ul.appendChild(queryButton);

   var mainDiv = document.getElementById("mainDiv");
   utils.removeChildren(mainDiv);

/*
   //add title
   var h1 = document.createElement("h1");
   h1.setAttribute("id","compositeTitle");
   var text = document.createTextNode("Query: "+args["collection"]);
   h1.appendChild(text);
   mainDiv.appendChild(h1);
*/
   mainDiv.appendChild(ul);
}

/************************************************************
 * Callback for a snapshot data from aqueti.js
 *
 * If we have a single snapshot call this function
 ************************************************************/
var aqSnapCallback = function(args)
{
   //The data needs to be pushed to the snapshot feature
   //call collection with image id
   args.collection = "composites";
   args.snapshot = args.data[0];
   args.query={"id":args.data[0]["imageId"]};
   args.sort = {};

   args.data = null;

   db.getData(args, aqCompositeCallback);
}

/************************************************************
 * Callback for a data request from aqueti.js
 *
 * If we have a single composite, call this function
 ************************************************************/
var aqCompositeCallback =  function(args)
{
   var items=args["data"].length;

   //If no items returns, call the error function
   if( items < 1)
   {
      aqError("No image was found");
      return;
   }

   //If more than one item is found, call the Query function
   if( items > 1)
   {
      //get template for teh specified type
      db.getQueryTemplate(args,genQueryForm);
      return;
   }

   //Convert array into an item
   var item = args["data"][0];

   var height = +utils.getDocumentHeight();

   //Normal composite processing
   var mainDiv = document.getElementById("mainDiv");
   mainDiv.setAttribute("style","width:100%;height:"+height+"px");
   mainDiv.setAttribute("imageId",item["id"]);

   var panoDiv = document.createElement("div");
   panoDiv.setAttribute("id","pano");
   panoDiv.setAttribute("style","width:100%;height:100%;");
   mainDiv.appendChild(panoDiv);

   if( "krpano" in item["outputFiles"] )
      var path=item["outputFiles"]["krpano"];
   else
   {
      alert("I do not know how to deal with these files: "+JSON.stringify(item["outputFiles"]));
   }

   /////////////////////////////////////////////
   // Create the krpano context
   /////////////////////////////////////////////
   var params = 
   {
      swf: path+"/pano.swf",
      xml: path+"/interactive.xml",
      target: "pano",
      html5: "prefer",
      passQueryParameters: true,
      id: "krpano"
   }
   embedpano( params );

   ai = new AI();
   ai.init("krpano", true);

   //create title and add to the mainDiv
   var h1 = document.createElement("h1")
   h1.setAttribute("id","compositeTitle");
   var text = document.createTextNode(item["title"]);
   h1.appendChild(text);
   mainDiv.appendChild(h1);

   //create interface div
   var ifaceDiv = document.createElement("div");
   ifaceDiv.setAttribute("id","ifaceDiv");
   mainDiv.appendChild(ifaceDiv);

   //Add info button
   var infoButton = document.createElement("button");
   var text = document.createTextNode("infoButton");
   infoButton.appendChild(text);
   infoButton.setAttribute("title",item["id"]);
   infoButton.setAttribute("id","infoButton");
   ifaceDiv.appendChild(infoButton);

   //Add snapshot button
   var snapButton = document.createElement("button");
   var text = document.createTextNode("SnapShot");
   snapButton.appendChild(text);
   snapButton.setAttribute("title",item["id"]);
   snapButton.setAttribute("id","snapButton");
   ifaceDiv.appendChild(snapButton);

   //Create infobox and hide
   var infoDiv = document.createElement("div");
   infoDiv.setAttribute("id", "infoDiv");
   infoDiv.setAttribute("hidden",true);
   var p = document.createElement("p");
   p.innerHTML="Date: "+item["date"]+
         "<br>Time: "+item["time"]+
         "<br>Description:"+item["description"]+
         "<br>Embed Code:<br>"+genEmbedCode(item);
   
   infoDiv.appendChild(p);

   mainDiv.appendChild(infoDiv);

   //Check if we're a snapshot, if so move to appropriate place
   if( "snapshot" in args)
   {
      ai.setView(args["snapshot"]["view"]);

      var mainDiv = document.getElementById("mainDiv");
      args["snapshot"]["edit"] = false;
      var snapDiv = generateSnapDiv(args["snapshot"]);
      mainDiv.appendChild(snapDiv);

      $("#snapDiv").show();
   }

}

/************************************************************
 * function to generate an embed code from a composite image
 ************************************************************/
function genEmbedCode( item )
{
   var code = "&ltiframe src=&quot"+item["outputFiles"]["krpano"]+"/index.html&quot seamless=true width=&quot100%&quot height=&quot500px&quot&gt&lt/iframe&gt";

   return code;
}

/************************************************************
 * Callback for a query with multiple results
 ************************************************************/
var aqQueryCallback =  function(args)
{
   $("#queryList").hide();

   //If we're an album, then generate a UL for each item
   if(args.collection == "albums")
   {
      genAlbumList(args["data"], "Query Result");
      return;
   }
   else if(args.collection == "composites")
   {
      genCompositeList(args["data"]);
      return;
   }
   else if(args.collection == "snapshots")
   {
      genSnapList(args["data"]);
      return;
   }


   //If we found one item, redirect to display that item
   if( args["data"].length == 1)
   {
      window.location.href = "./index.html?"+args.collection+"="+args.data[0]["id"];
   }

   else
   	genCompositeList(args);

   //genImageList(args.data);

}

/************************************************************
 * Callback for an album request
 ************************************************************/
var aqAlbumCallback = function(args)
{
   //Check if more than one exists.
   if( args["data"].length > 1)
   {
      alert(args.length +" albums found!");
      aqQueryCallback(args);
      return;
   }

   //Check if no reults were found
   if(args["data"].length < 1)
   {
      aqError("No albums found");
      return;
   }

   //Check if the first element is an album
   if( args.data[0].items[0]["doctype"] == "album")
   {
      var alList = [];

      for( var i = 0; i < args.data[0].items.length; i++)
      {
         alList.push(args.data[0].items[i]["data"])
      }
  
      genAlbumList( alList,args.data[0].title);
      return;
   }

   //Otherwise, assume they are all composites


   //Single album, let's render!
   var mainDiv = document.getElementById("mainDiv");

   //Remove all children from mainDiv and set to horizontal
   utils.removeChildren(mainDiv);

   //If we have only one element, make vertical
   mainDiv.setAttribute("class","vertical");
   mainDiv.setAttribute("imageId",item["id"]);

   //Create the album header
   var headerDiv = document.createElement("div");
   headerDiv.setAttribute("id","header");
   var h1 = document.createElement("h1");

   if( typeof args["data"][0].title != 'undefined')
      h1.innerHTML = args["data"][0].title;
   else
      h1.innerHTML = "Album";

   headerDiv.appendChild(h1);
   mainDiv.appendChild(headerDiv);

   //Create ul for non-album list
   var ul = document.createElement("ul");

   //Loop through items. Create new UL for albums, add to ul for other
   for( var i = 0; i < args.data[0]["items"].length; i++)
   {
      if(args.data[0]["items"][i]["doctype"] == "album")
      {
         var ul2 = genAlbumView( args.data[0]["items"][i]["data"]);
         mainDiv.appendChild(ul2);
      }
      else
      {
         var li = genCompositeLI( args["data"][0]["items"][i]["data"]);
         ul.appendChild(li);
      }
   }

   mainDiv.appendChild(ul);


/*
   //We have the header, let's add the data
   for( var i = 0; i < args["data"][0]["items"].length; i++)
      genAlView( args["data"][0]["items"][i]["data"]);
*/
}

/************************************************************
 * genCompositeLI
 *
 * Creates a UL for each album in a list
 *********************************a***************************/
function genCompositeLI( data)
{
   var li = document.createElement("li");
   var a = document.createElement("a");
   a.href = "index.html?composites="+data["id"];

   //Create image for display (full scale items)
   var img = document.createElement("img");
   if( data["preview"] != "undefined")
      img.setAttribute("src",data["preview"]);
   img.setAttribute("alt",data["title"]);
   a.appendChild(img);

   li.appendChild(a);

   return li;
}

/************************************************************
 * genAlView
 *
 * Creates a UL for each album in a list
 *********************************a***************************
function genAlView( data )
{
   //Single album, let's render!
   var mainDiv = document.getElementById("mainDiv");

   var ul = document.createElement("ul");

   for( var i = 0; i < data.length; i++)
   {
      if( data
   }

   

      if(args.data[0]["items"][i]["doctype"] == "album")
      {
         alert("Doctype:"+JSON.stringify(args.data[0]["items"][i]));
      }
      else
      {
        var ul = genAlbumView(args.data[0]);
        if( utils.isObject(ul))
           mainDiv.appendChild(ul);
      }
   }

   launchViewListeners();
   return;
}
*/
/************************************************************
 * genAlbumList
 *
 * Creates a UL for each album in a list
 *********************************a***************************/
function genAlbumList(data, title)
{
   //Normal composite processing
   var mainDiv = document.getElementById("mainDiv");

   //Remove all children from mainDiv and set to horizontal
   utils.removeChildren(mainDiv);
   mainDiv.setAttribute("class","horizontal");

   //Create the album header
   var headerDiv = document.createElement("div");
   headerDiv.setAttribute("id","header");
   var h1 = document.createElement("h1");

//if (typeof variable === 'undefined') {
    // variable is undefined
//}
   if( typeof data.title != 'undefined')
      h1.innerHTML = data.title;
   else
      h1.innerHTML = title;

   headerDiv.appendChild(h1);
   mainDiv.appendChild(headerDiv);
   
   //Generate a UL for each album
   for( var i = 0; i < data.length; i++)
   {
/*
      //Check if we have an array of images
      if( utils.isArray(data[i].items))
      {
         for( var j = 0; j < data[i].items.length; j++)
         {
            var ul = genAlbumView(data[i].items[j]["data"]);
  
            if( utils.isObject(ul))
               mainDiv.appendChild(ul);
         }
      }
*/
         var ul = genAlbumView(data[i]);

         if( utils.isObject(ul))
            mainDiv.appendChild(ul);
   }

   launchViewListeners();
}

/************************************************************
 * genAlbumView
 *
 * Creates a UL for the given album
 *********************************a***************************/
function genAlbumView(data)
{
   var ul = document.createElement("ul");

/*
   //Create Albums title
   var li = document.createElement("li");
   var a = document.createElement("a");
   a.href = "index.html?albums="+data["id"];
   var h3 = document.createElement("h3");
   h3.innterHTML = data["title"];
   a.appendChild(h3);
   li.appendChild(a);
   ul.appendChild(li);
*/
   //Create image array
   for( var i = 0; i < data["items"].length; i++)
   {
      var item = data["items"][i]["data"];

      var listItem = document.createElement("li");

      //Generate components
      var a = document.createElement("a");

      //a.href = "./index.html?albums="+data["id"]+"#"+i;
      //sdf - fix
      if( item["type"] == "album") 
         a.href = "./index.html?albums="+item["id"]+"#"+i;
      else if( item["type"] == "composite") 
         a.href = "./index.html?composites="+item["id"]+"#"+i;
      else if( item["type"] == "snapshot") 
         a.href = "./index.html?snapshots="+item["id"]+"#"+i;
      else
         a.href = "./index.html?albums="+data["id"]+"#"+i;

      //Create image for display (full scale items)
      var img = document.createElement("img");
      if( item["preview"] != "undefined")
         img.setAttribute("src",item["preview"]);
      img.setAttribute("alt",item["title"]);
      a.appendChild(img);


/* iframe solution
      //create iframe for static context
      var frame = document.createElement("iframe");
      frame.setAttribute("src",args.data[i]["outputFiles"]["krpano"]+"/static.html");     
      frame.setAttribute("width","500px");
      frame.setAttribute("height","200px");
      a.appendChild(frame)
*/

/* Uncomment for individual image titles 
      var h2 = document.createElement("h2");
      h2.innerHTML = data[i]["title"];
      a.appendChild(h2);
*/
      listItem.appendChild(a);

      ul.appendChild(listItem);
   }

   return ul;
}

/************************************************************
 * If we have a single album, call this function
 *********************************a***************************/
var genCompositeList =  function(data)
{
   var items=data.length;

   //If no items returns, call the error function
   if( items < 1)
   {
      aqError("Query: Item Not Found");
      return;
   }


   //Normal composite processing
   var mainDiv = document.getElementById("mainDiv");

   //Remove all children from mainDiv and set to horizontal
   utils.removeChildren(mainDiv);
   mainDiv.setAttribute("class","horizontal");
   mainDiv.setAttribute("imageId",item["id"]);


   var headerDiv = document.createElement("div");
   headerDiv.setAttribute("id","header");
   var h1 = document.createElement("h1");
   h1.innerHTML = "Query result";

   headerDiv.appendChild(h1);
   mainDiv.appendChild(headerDiv);


   var ul = document.createElement("ul");
   mainDiv.appendChild(ul);

   //Loop through all returned items to generate a list
   for( var i = 0; i<items; ++i)
   {
      var listItem = document.createElement("li");

      //Generate components
      var a = document.createElement("a");
      a.href = "./index.html?composites="+data[i]["id"];

      //Create image for display (full scale items)
      var img = document.createElement("img");
      if( data[i]["preview"] != "undefined")
         img.setAttribute("src",data[i]["preview"]);
      img.setAttribute("alt",data[i]["title"]);
      a.appendChild(img);


/* iframe solution
      //create iframe for static context
      var frame = document.createElement("iframe");
      frame.setAttribute("src",args.data[i]["outputFiles"]["krpano"]+"/static.html");     
      frame.setAttribute("width","500px");
      frame.setAttribute("height","200px");
      a.appendChild(frame)
*/
      var h2 = document.createElement("h2");
      h2.innerHTML = data[i]["title"];

      a.appendChild(h2);
      listItem.appendChild(a);

      ul.appendChild(listItem);
   }

   launchViewListeners();
}

var aqError = function(msg)
{
   alert("Error:"+msg);
}

/***********************************************************
 * genUL
 *
 * function to generate an unordered list instead of using form
 ***********************************************************/
function genUL( template, item)
{
   //Create the unordered list
   var ul = document.createElement("ul");

   //Loop through all of the keys in the template and
   //generate the appropriate item
   for( var key in template)
   {
      if(item==undefined)
         var li = genInput( template[key],{},key);
      else
         var li = genInput( template[key],item[key], key);

      ul.appendChild(li);
   }
   return ul;
}

/***********************************************************
 * genInput
 *
 * Function to generate the input Form
 *
 * Steps through all template component provided.
 ************************************************************/
function genInput(template, item, key)
{
   //Create an li component
   var li = document.createElement("li");

   /////////////////////////////////////////////
   //Generate a dictionary UL
   /////////////////////////////////////////////
   if(template["type"] == "dictionary")
   {
      var ul2 = genUL(template["data"], item, key);
      ul2.setAttribute("title",key);
      ul2.setAttribute("class","dict");

      var text = document.createTextNode(key);

      li.appendChild(text);
      li.appendChild(ul2);
   }

   /////////////////////////////////////////////
   // Generate an array ul
   /////////////////////////////////////////////
   else if( template["type"] =="array")
   {
      //Create a ne ul element
      var ul = document.createElement("ul");
      ul.setAttribute("class","array");
      ul.setAttribute("title",key);

      //Key key if it does not exist make it an empty array
      if( !utils.isArray(item))
         item = [];

      //Add text to descript li
      var text = document.createTextNode(key)
      li.appendChild(text);

      if(item.length == 0)
      {
         item.push("");
      }
      //Loop through the array and generate an li for each
      if( item.length > 0)
      {
         for( var i = 0; i < item.length; i++ )
         {
            var li2 = document.createElement("li");
            var text = document.createTextNode(i);
            li2.appendChild(text);

            //sdf - perhaps we shoudl 
            //generate an UL 
            var ul2 = genUL( template["data"],item[i], key)
            ul2.setAttribute("index",i);
            ul2.setAttribute("class","group");

            li2.appendChild(ul2);
            ul.appendChild(li2);
         }

         //Create add button
         var addButton = document.createElement("button");
         var text = document.createTextNode("Add");
         addButton.appendChild(text);
         addButton.setAttribute("title",key);
         addButton.setAttribute("id","addButton");

         li.appendChild(ul);
         li.appendChild(addButton);
      }
   }
   /////////////////////////////////////////////
   // If input is select type
   /////////////////////////////////////////////
   else if( template["type"] == "select")
   {
      var select = genDropDownList( key,key,template["options"]);
      select.setAttribute("title",key);
      if(template["key"] == true)
         select.setAttribute("key",true);

      for( var value in template["options"])
      {
         if( item == template["options"][value])
         {
            $(select).val(item);
         }
      }

      li.innerHTML = key;
      li.appendChild(select);
   }

   /////////////////////////////////////////////
   // If all else fails, use normal text input
   /////////////////////////////////////////////
   else
   {
      //Normal processing
      var input = document.createElement("input");
      input.setAttribute("type","text");
      if(template["key"] == true)
         select.setAttribute("key",true);

      if(item == undefined)
         input.setAttribute("value","");
      else if( utils.isObject(item ))
      {
         if(item == undefined)
            input.setAttribute("value","");
         else
            input.setAttribute("value",item[key]);
      }
      else
         input.setAttribute("value",item);

      input.setAttribute("name",key);
      input.setAttribute("title",key);

      //check if readonly
      if( template["edit"] == false)
      {
         input.setAttribute("readonly",true);
         input.setAttribute("disable",true);
      }

      li.innerHTML=key;
      li.appendChild(input);
   }
   return li;
}

/************************************************************
 * Generate an dropdown list
 ************************************************************/
function genDropDownList( name, id, options )
{
   var select = document.createElement("select");

   for( var i = 0; i < options.length; i++ )
   {
      var opt = document.createElement("option");
      var text = document.createTextNode(options[i]);
      opt.appendChild(text);

      select.appendChild(opt);
   }

   select.setAttribute("id",id);
   select.setAttribute("name",name);

   return select;
}

/************************************************************
 * function to get a list of images
 *
 * This function gets a list of images from the database
 ************************************************************/
function genImageList( data )
{
   var home = "";
   
   for( var i = 0; i<data.lengths; ++i)
   {
      home = "";
               
      var listItem = document.createElement("li");
   
      //Generate components
      var url=data[i]["outputFiles"]["krpano"];
      url = home+url.replace(/"/g,"");
   
      //This is for Cameron
      var link = "<a href=\""+url+"/index.html\"></a>";
      var div = "<div class=\"title\">"+data[i]["title"]+"</div>";
      var img = "<img src=\""+url+"/preview.jpg\" />"; 
      var embed = "<a href=\""+url+"/index.html\"><iframe width=100% height=100% src=\""+link+"\"></iframe></a>";
      var embed2 = "&lt;iframe width=100% height=50% src=\""+url+"/index.html\"&gt;&lt;/iframe&gt;";
   
   	if( "title" in data[i])
      {
   	   var item = "<a href=\""+url+"/index.html\">"+img+"<h2>"+data[i]["title"]+"</h2></a>";
      }
      else
      {
   	   var item = "<a href=\""+url+"/index.html\">"+img+"</a>";
      }
   
      listItem.innerHTML = item;
      listElement.appendChild(listItem);
   }
}


/************************************************************
 * Interface functions
 ************************************************************/
/************************************************************
 * view listeners
 *
 * Funcion to extract data from long list
 ************************************************************/
 function launchViewListeners()
 {
   //Cameron's interface controls
   $('.horizontal ul').on('mousemove', function(e) 
   {
      if (e.pageX >= $(window).width() * .8 && timeOut === null) 
      {
         scroll = $(this).scrollLeft();
         scrollLeft($(this));
      } 
      else if (e.pageX <= $(window).width() * .2 && timeOut === null) 
      {
         scroll = $(this).scrollLeft();
         scrollRight($(this));
      }
      else if (e.pageX < $(window).width() * .8 && e.pageX > $(window).width() * .2 && timeOut !== null) 
      {
         window.clearInterval(timeOut);
         timeOut = null;
      }
   });

   $('.horizontal ul').mouseleave(function() 
   {
      window.clearInterval(timeOut);
      timeOut = null;
   });
}

function scrollLeft(elem) {
    timeOut = window.setInterval(function() {
        scroll += 15;
        if (scroll > elem[0].scrollWidth - elem.width())
            scroll = elem[0].scrollWidth - elem.width();
        elem.scrollLeft(scroll);
    }, 25);
}

function scrollRight(elem) {
    timeOut = window.setInterval(function() {
        scroll -= 15;
        if (scroll < 0)
            scroll = 0;
        elem.scrollLeft(scroll);
    }, 25);
}

$(function() {
    $('.horizontal ul').on('mousemove', function(e) {
        if (e.pageX >= $(window).width() * .8 && timeOut === null) {
            scroll = $(this).scrollLeft();
            scrollLeft($(this));
        } else if (e.pageX <= $(window).width() * .2 && timeOut === null) {
            scroll = $(this).scrollLeft();
            scrollRight($(this));
        } else if (e.pageX < $(window).width() * .8 && e.pageX > $(window).width() * .2 && timeOut !== null) {
            window.clearInterval(timeOut);
            timeOut = null;
        }
    });

    $('.horizontal ul').mouseleave(function() {
        window.clearInterval(timeOut);
        timeOut = null;
    });
});


