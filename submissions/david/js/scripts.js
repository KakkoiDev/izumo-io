function getTxtValue() {
  // get element TEXTAREA
  const userValue = document.getElementById("txtAreaInput");

  //get value from TEXTarea
  const userTxtValue = userValue.value;

  // Ollama serve send mesage
   fetch('http://192.168.1.244:11434/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'dolphin3:latest', // MODEL
          prompt: userTxtValue,  //messege
          stream: false,
        }),
      })
      .then(response => response.json())
      .then(data => {
          console.log(data)

          //ollama retur
          const aiResponse = data.response

          //HTML element for AI message
          const aiDiv = document.createElement("DIV");
          aiDiv.className = "aiDiv"

          const pAi = document.createElement("p")
          pAi.textContent = aiResponse

          //put elements on screen
          aiDiv.appendChild(pAi)
          mainDiv.appendChild(aiDiv)

        }) // response
      .catch(error => console.error('Error:', error));


  // create a HTML elements with the value
  const userTxtDiv = document.createElement("DIV");
  userTxtDiv.className = "userTxtDiv";

  const pTextUser = document.createElement("p");
  const pTextUserValue = document.createTextNode(userTxtValue);

  //ADD DIV on MAN div
  pTextUser.appendChild(pTextUserValue);
  userTxtDiv.appendChild(pTextUser);
  mainDiv.appendChild(userTxtDiv);

  // clear text input
  userValue.value = "";

  // cursor go back on text area
  userValue.focus();
}

window.getTxtValue = getTxtValue;

