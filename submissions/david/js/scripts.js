function getTxtValue() {
  // get element TEXTAREA
  const userValue = document.getElementById("txtAreaInput");

  //get value from TEXTarea
  const userTxtValue = userValue.value;

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
