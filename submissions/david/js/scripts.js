function getTxtValue() {
  const mainDiv = document.getElementById("mainDiv");
  const spinner = document.getElementById("spinner");
  const userValue = document.getElementById("txtAreaInput");

  const userTxtValue = userValue.value.trim();
  if (!userTxtValue) return;

  // show messages to user
  const userTxtDiv = document.createElement("div");
  userTxtDiv.className = "userTxtDiv";
  userTxtDiv.innerHTML = `<p>${userTxtValue}</p>`;
  mainDiv.appendChild(userTxtDiv);

  // show spinner
  spinner.style.display = "block";

  // send reguest to  API
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
      spinner.style.display = "none"; // hide spinner

      const aiResponse = data.response || "(sem resposta)";
      const aiDiv = document.createElement("div");
      aiDiv.className = "aiDiv";

      // break lines on \n\n
      aiDiv.innerHTML = `<p>${aiResponse.replace(/\n/g, "<br>")}</p>`;

      mainDiv.appendChild(aiDiv);
    })
    .catch((err) => {
      spinner.style.display = "none";
      console.error(err);

      const errDiv = document.createElement("div");
      errDiv.className = "aiDiv error";
      errDiv.innerHTML = "<p>Erro ao conectar ao servidor.</p>";
      mainDiv.appendChild(errDiv);
    });

  // clear textArea and focus
  userValue.value = "";
  userValue.focus();
}

window.getTxtValue = getTxtValue;
