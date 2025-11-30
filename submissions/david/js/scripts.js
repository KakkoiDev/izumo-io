function getTxtValue() {
  const mainDiv = document.getElementById("mainDiv");
  const userValue = document.getElementById("txtAreaInput");

  const userTxtValue = userValue.value.trim();
  if (!userTxtValue) return;

  // show messages to user
  const userTxtDiv = document.createElement("div");
  userTxtDiv.className = "userTxtDiv";
  userTxtDiv.innerHTML = `<p>${userTxtValue}</p>`;
  mainDiv.appendChild(userTxtDiv);

  // AI PLACEHOLDER and SPINNER 
  const aiDiv = document.createElement("div");
  aiDiv.className = "aiDiv";

  const spinner = document.createElement("div");
  spinner.className = "spinner";

  aiDiv.appendChild(spinner);
  mainDiv.appendChild(aiDiv);

  // Scroll down when add AI messages
  mainDiv.scrollTop = mainDiv.scrollHeight;

  // send reguest to  API server
  fetch("http://192.168.1.244:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "dolphin3:latest",
      prompt: userTxtValue,
      stream: false,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const aiResponse = data.response || "(sem resposta)";

      // remove spinner
      aiDiv.removeChild(spinner);

      // add response text
      const p = document.createElement("p");
      p.innerHTML = aiResponse.replace(/\n/g, "<br>");

      aiDiv.appendChild(p);

      mainDiv.scrollTop = mainDiv.scrollHeight;

    })
    .catch((err) => {
       aiDiv.removeChild(spinner);
      aiDiv.innerHTML = "<p>Erro ao conectar ao servidor.</p>";
      console.error(err);
    });

  // clear textArea and focus
  userValue.value = "";
  userValue.focus();
}

window.getTxtValue = getTxtValue;
