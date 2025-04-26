var scenes = document.getElementsByClassName("scene");
var switchScene = function (index) {
  for (var i = 0; i < scenes.length; i++) {
    scenes[i].style.display = "none";
  }
  window.scroll(0, 0);
  scenes[index].style.display = "block";
  scenes[index].style.animation = "1s fade-in forwards";
};
switchScene(0);

document.getElementById("send-btn").addEventListener("click", function () {
  var userMessage = document.getElementById("user-textarea").value;
  if (!userMessage.trim()) return;

  document.getElementById("user-textarea").value = "";

  var chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += "<p><strong>You:</strong> " + userMessage + "</p>";

  document.getElementById("loading").style.display = "block";

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("loading").style.display = "none";
      if (data.response) {
        chatBox.innerHTML +=
          "<p><strong>Bot:</strong> " + data.response + "</p>";
      } else if (data.error) {
        chatBox.innerHTML +=
          "<p><strong>Error:</strong> " + data.error + "</p>";
      } else {
        chatBox.innerHTML +=
          "<p><strong>Error:</strong> Unexpected response.</p>";
      }
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch((error) => {
      document.getElementById("loading").style.display = "none";
      chatBox.innerHTML +=
        "<p><strong>Error:</strong> " + error.message + "</p>";
      chatBox.scrollTop = chatBox.scrollHeight;
    });
});
