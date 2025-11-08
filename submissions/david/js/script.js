
        const divInput = document.getElementById("divInput")

        const txtDiv = document.createElement("div");
        
        const txtInput = document.createElement("input")
        txtInput.type = "text"
        txtInput.placeholder = "type here..."

        const btnSend = document.createElement("input")
        btnSend.type = "submit"
        btnSend.value = "SEND"
        btnSend.className = "btn"

        
        txtDiv.appendChild(txtInput)
        txtDiv.appendChild(btnSend)
        divInput.appendChild(txtDiv)
        