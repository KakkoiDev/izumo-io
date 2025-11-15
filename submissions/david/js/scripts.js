function getTxtValue() {
  // get value TEXTAREA
  const userTxtDivValue = document.getElementById("txtAreaInput").value;

  // create a HTML elements with the value
  const userTxtDiv = document.createElement("DIV");
  userTxtDiv.className = "userTxtDiv";

  const pTextUser = document.createElement("p");
  const pTextUserValue = document.createTextNode(userTxtDivValue);

  //ADD DIV on MAN div
  pTextUser.appendChild(pTextUserValue);
  userTxtDiv.appendChild(pTextUser);
  mainDiv.appendChild(userTxtDiv);

  // clear text input
  txtInput.value = "";
}
