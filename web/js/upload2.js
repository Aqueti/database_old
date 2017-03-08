var step = 100000
function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // files is a FileList of File objects. List some properties.
    var output = [];
    for (var i = 0, f; f = files[i]; i++) {
      output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
                  f.size, ' bytes, last modified: ',
                  f.lastModifiedDate ? f.lastModifiedDate.toLocaleDateString() : 'n/a',
                  '</li>');
    }
    document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

//document.getElementById('files').addEventListener('change', handleFileSelect, false);
var sendFileCallback = function(FD)
{
   FD.count = FD.count + 1;

   //if we're close to the end
   if( FD.done == true)
   {
      FD.object = null;
      alert("Upload complete:"+FD["result"]["url"]);
      return;
   }
   //in the middle
   else if( FD.stop+step < FD.end)
   {
      FD.name = FD.result.name;
      FD.start = FD.stop;
      FD.stop= FD.stop+step;
   }
   //We're in our last send
   else if( FD.stop+step>= FD.end)
   {
      FD.name = FD.result.name;
      FD.start = FD.stop;
      FD.stop= FD.end;
      FD.done = true;
   }

   readBlob(FD);
}

function readBlob(FD) 
{

    var reader = new FileReader();

    // If we use onloadend, we need to check the readyState.
    reader.onloadend = function(evt) 
    {
      if (evt.target.readyState == FileReader.DONE) 
      { // DONE == 2

        //Get file type
        var buffer = evt.target.result;
        var int32View = new Int32Array(buffer);

        FD.object = {};
        FD.object.data = btoa(evt.target.result);

        if( FD.file.name.indexOf("tif") != -1)
           FD.object["ext"] = "tif";
        else
           FD.object["ext"] = "jpg";
        
        if(FD.done == true)
           FD.object["end"] = true;
        else
           FD.object["end"] = false;
        if( FD.start == 0 )
        {
           FD.object["start"] = true;
           FD.count = 0;
        }
        else
           FD.object["start"] = false;
           FD.object["name"] = FD.name;

        db.sendFile(FD, sendFileCallback);
      }
    };
    blob = null;

    var blob = FD.file.slice(FD.start, FD.stop + 1);
    reader.readAsBinaryString(blob);
}

function readFile()
{
   //Get data 
  var files = document.getElementById('files').files;

   if (!files.length) 
   {
      alert('Please select a file!');
      return;
   }


   //Create a common structure for writing to file
   var FD = {};
   FD.file = files[0];
   FD.start = 0;
   FD.end = FD.file.size - 1;
   FD.stop = step;
   FD.done = false;

   readBlob(FD);
}


  
document.querySelector('.readBytesButtons').addEventListener('click', function(evt) {
    if (evt.target.tagName.toLowerCase() == 'button') {
      var startByte = evt.target.getAttribute('data-startbyte');
      var endByte = evt.target.getAttribute('data-endbyte');
      readFile();
    }
  }, false);
