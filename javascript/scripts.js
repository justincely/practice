window.onload = initAll;
//window.onload = displayAlert();
//window.onload = writeMessage;


function initAll(){
  document.getElementById("redirect").onclick = initRedirect;
}

function initRedirect() {
  window.location = "jswelcome.html";
  return false;
}

function writeMessage() {
  document.getElementById("helloMessage").innerHTML = "Hello, world!";
}

function displayAlert(){
  alert("AHHHHHH!");
}
