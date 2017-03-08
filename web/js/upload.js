function fileSelected() {
var file = document.getElementById('fileToUpload').files[0];
 if (file) {
var fileSize = 0;
if (file.size > 1024 * 1024)
fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
 else
fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

document.getElementById('fileName').innerHTML = 'Name: ' + file.name;
document.getElementById('fileSize').innerHTML = 'Size: ' + fileSize;
document.getElementById('fileType').innerHTML = 'Type: ' + file.type;
 }
}

var sendCallback = function(args)
{
   alert("Sent");
}

function uploadFile() 
{
   var fd = document.getElementById('fileToUpload');
   var name = fd.value;

   var oReq = new XMLHttpRequest();
   oReq.open("GET", name, true);
   oReq.response = "blob";

   oReq.onload = function(oEvent)
   {
      var blob = oReq.response;
      var fd = {};
      fd.name = name;
      fd.data = blob;
      db.sendFile( args, sendCallback);
   }

   oReq.send();

 
 /*
   var xhr = new XMLHttpRequest();
   xhr.upload.addEventListener("progress", uploadProgress, false);
   xhr.addEventListener("load", uploadComplete, false);
   xhr.addEventListener("error", uploadFailed, false);
   xhr.addEventListener("abort", uploadCanceled, false);
   xhr.open("POST", "UploadMinimal.aspx");
   xhr.send(fd);
*/
}



function uploadProgress(evt) {
 if (evt.lengthComputable) {
 var percentComplete = Math.round(evt.loaded * 100 / evt.total);
document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
 }
else {
 document.getElementById('progressNumber').innerHTML = 'unable to compute';
}
}

function uploadComplete(evt) {
/* This event is raised when the server send back a response */
 alert(evt.target.responseText);
}

 function uploadFailed(evt) {
alert("There was an error attempting to upload the file.");
 }

 function uploadCanceled(evt) {
 alert("The upload has been canceled by the user or the browser dropped the connection.");
}

