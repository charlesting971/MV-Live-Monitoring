var socket = io.connect('http://' + document.domain + ':' + location.port); 
// Button to initiate Data Fetching
function startLive() {
  console.log('Fetching Data From Server...');
  socket.emit('requestFromClient');
  var stopLiveButton=document.getElementById("stopLiveButton");
  stopLiveButton.style.display="inline-block";
  stopLiveButton.style.backgroundColor="#8B0000";
}
// Button to stop Data Fetching
function stopLive() {
  console.log('Stopped Fetching Data From Server...');
  socket.emit('stoprequestFromClient');
}