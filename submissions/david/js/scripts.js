 //select DIV to insert chat elements
        const divInput = document.getElementById("divInput")
        const mainDiv = document.getElementById("mainDiv")

        function getTxtValue() {
        // get value TEXTAREA 
            const userTxtDivValue = document.getElementById('txtAreaInput').value

            // create a HTML elements with the value
            const userTxtDiv = document.createElement("DIV")
            userTxtDiv.className = "userTxtDiv"

            const pTextUser = document.createElement("p")
            const pTextUserValue = document.createTextNode(userTxtDivValue)
            

            //ADD DIV on MAN div
            pTextUser.appendChild(pTextUserValue)
            userTxtDiv.appendChild(pTextUser)
            mainDiv.appendChild(userTxtDiv)

            // clear text input
            txtInput.value = ""
        }


        // create new DIV 
        const txtDiv = document.createElement("div");
        txtDiv.className = "txtDiv"
                    
        //crete INPUT TEXT
        const txtInput = document.createElement("textarea")
        txtInput.id = "txtAreaInput"
        txtInput.className = "txtArea"
        txtInput.placeholder = "type here..."



        // SUBMIT button
        const btnSend = document.createElement("input")
        btnSend.type = "submit"
        btnSend.value = "SEND"
        btnSend.className = "btn"
        btnSend.onclick = getTxtValue

        //ADD elements on DOM
        txtDiv.appendChild(txtInput)
        txtDiv.appendChild(btnSend)
        divInput.appendChild(txtDiv)