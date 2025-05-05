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

let selectedPersona = localStorage.getItem("persona") || "default";

function selectPersona(personaKey) {
  selectedPersona = personaKey;
  localStorage.setItem("persona", personaKey);
  switchScene(0);
  document.getElementById("greeting").innerHTML = `
  <img src="/static/android-chrome-512x512.png" alt="EldiiarBot" width="100" />
  <h1 style="margin: 10px 0 30px 0px; font-weight: 300; color: #fff">
   Hello, I am <b style="font-weight: 500; color: #fff">EldiiarBot</b>! What's on your mind today?
  </h1> 
  <p>You’re chatting with <b style="font-weight: 500; color: #fff"><span class="material-symbols-rounded">smart_toy</span> ${selectedPersona
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase())}
</b>.</p>
`;
}
selectPersona(selectedPersona);

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
    body: JSON.stringify({ message: userMessage, persona: selectedPersona }),
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

var form = document.getElementById("my-form");

async function handleSubmit(event) {
  event.preventDefault();
  var status = document.getElementById("my-form-status");
  var data = new FormData(event.target);
  fetch(event.target.action, {
    method: form.method,
    body: data,
    headers: {
      Accept: "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        status.innerHTML = "Thanks for your submission!";
        form.reset();
      } else {
        response.json().then((data) => {
          if (Object.hasOwn(data, "errors")) {
            status.innerHTML = data["errors"]
              .map((error) => error["message"])
              .join(", ");
          } else {
            status.innerHTML = "Oops! There was a problem submitting your form";
          }
        });
      }
    })
    .catch((error) => {
      status.innerHTML = "Oops! There was a problem submitting your form";
    });
}
form.addEventListener("submit", handleSubmit);
window.onbeforeunload = () => {
  for (const form of document.getElementsByTagName("form")) {
    form.reset();
  }
};
