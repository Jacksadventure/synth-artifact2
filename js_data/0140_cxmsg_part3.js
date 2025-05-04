        const estilo_tituloCxmsg=
            "display: flex;"+
            "justify-content: flex-start;"+
            "align-items: center;"+
            "width: 100%;"+
            "background-color:"+this.cor+";"+
            "color:#fff;"+
            "padding:5px;"+
            "border-radius:5px 5px 0px 0px"
        const tituloCxmsg=document.createElement("div")
        tituloCxmsg.setAttribute("style",estilo_tituloCxmsg)
        tituloCxmsg.innerHTML=this.titulo
        areaCxmsg.appendChild(tituloCxmsg)