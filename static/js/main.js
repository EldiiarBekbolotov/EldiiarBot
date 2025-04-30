// (c) 2025 Eldiiar Bekbolotov. Licensed under the MIT License.
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

document.getElementById("send-btn").addEventListener("click", sendMessage);

document
  .getElementById("user-textarea")
  .addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  });

let timerInterval;
let timer = 0;
function startTimer() {
  timerInterval = setInterval(function () {
    timer += 0.01;
    document.getElementById("timer").innerText = timer.toFixed(2);
  }, 10);
}
function resetTimer() {
  clearInterval(timerInterval);
  timer = 0;
  document.getElementById("timer").innerText = timer.toFixed(2);
}
function sendMessage() {
  document.getElementById("greeting").style.display = "none";
  resetTimer();
  startTimer();

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
      resetTimer();
      if (data.response) {
        chatBox.innerHTML +=
          "<p><strong>EldiiarBot:</strong> " + data.response + "</p>";
      } else if (data.error) {
        chatBox.innerHTML +=
          '<p><img src="/static/android-chrome-512x512.png" alt="EldiiarBot" class="logo-icon"/><strong>EldiiarBot:</strong> It seems that there has been an error trying to fetch the data you requested. Please try again later. Error type: ' +
          data.error +
          "</p>";
      } else {
        chatBox.innerHTML +=
          "<p><strong>EldiiarBot:</strong> It seems that there has been an error trying to fetch the data you requested. Please try again later. Error type: Unexpected response.</p>";
      }
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch((error) => {
      document.getElementById("loading").style.display = "none";
      resetTimer();
      chatBox.innerHTML +=
        '<p><img src="/static/android-chrome-512x512.png" alt="EldiiarBot" class="logo-icon"/><strong>EldiiarBot:</strong> It seems that there has been an error trying to fetch the data you requested. Please try again later. Error type: ' +
        error.message +
        "</p>";
      chatBox.scrollTop = chatBox.scrollHeight;
    });
}
