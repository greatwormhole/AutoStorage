// Make the function wait until the connection is made...
function waitForSocketConnection(socket, msg){
    setTimeout(
        function () {
            if (socket.readyState === 1) {

                 socket.send(msg);

            } else {

                waitForSocketConnection(socket, msg);
            }

        }, 5);
}
///logout

function logout(ip){
    $.ajax({
        method:"POST",
        async: true,
        url: logout_url,
        data:{"ip": ip},
        success: function (response){
            location.href = home_url
            }
        })
}
/// authorization logic///
function authorized(){

    $('#login-BU').css('display','none')

}


function nonAuthorized(){

    $('#login-BU').css('display','block')
    $('.content').append('<h2 class="text" id="auth-prompt-text">Необходима авторизация!</h2>')
}

///prompt logic///
function promptHide(){
    $('#prompt-block-UI').hide()
    $('#prompt-content').children().remove()
}

/// choose THD screen///
function viewListOfTHD(){
    $.ajax({
        method:"GET",
        async: true,
        url: THDList,
        success: function (response){
            viewTHDList(response)
        }

    })
}
function viewTHDList(response){
    if ($('#prompt-block-UI').css('display') != 'none'){
    return
    }
    $('#prompt').css({'flex-direction':'column', 'border':'1px solid black', 'background-color':'white', 'border-radius':'10px 10px 10px 10px'})
    var html = ''
    html += "<div class = 'prompt-row'>"
    html += "<div class = 'prompt-cell'><span>Номер ТСД</span></div>"
    html += "<div class = 'prompt-cell'><span>IP ТСД</span></div>"
    html += "<div class = 'prompt-cell'></div>"
    html += "</div>"
    for (let i = 0; i<response.length; i++){

        html += "<div class = 'prompt-row'>"
        html += "<div class = 'prompt-cell' id='THD_"+response[i].fields.THD_number+"_num'><span>"+response[i].fields.THD_number+"</span></div>"
        html += "<div class = 'prompt-cell'><span>"+response[i].fields.ip+"</span></div>"
        if (!response[i].fields.is_using){
            html += "<div class = 'prompt-cell'><button class = 'positive' id='"+response[i].fields.THD_number+"' onclick='selectTHD(this, this.id)'>Выбрать</button></div>"
        } else{
            html += "<div class = 'prompt-cell'><button disabled>В работе!</button></div>"
        }
        html += "</div>"
    }

    $('#prompt-content').append(html)
    $('.prompt-cell').css({'flex-basis':'33.33%'})
    $('#prompt-name').text('Список доступных ТСД.')
    $('#prompt-block-UI').show()
}

function selectTHD(obj, id){
    $.ajax({
        method:"POST",
        async: true,
        url: THDSelect,
        data:{'THD_num':id, 'PC':1},
        success: function (response){
            $(obj).attr("disabled", 'disabled');
            $(obj).prop("onclick", null).off("click");
            $(obj).removeClass('positive')
            $(obj).text('В работе!')
            var wsStart = 'ws://',
                loc = window.location;
            if (loc.protocol == 'https:') {
                 wsStart = 'wss://'
            }
            var socket = new WebSocket(wsStart+window.location.hostname+':'+window.location.port+'/ws/THD-ws/'+id)
            setWSHandler(socket)
            /// test///
           /// $(socket).on('open', function(){
             ///   socket.send(JSON.stringify({"code":"101"}))
           /// })+
            /// test///
            $.ajax({
                method:"GET",
                url:THDCheck,
                data:{'id':id},
                success: function (response){

                    switch (response.status){
                        case true:
                            $('.prompt-message-text').text('Отсканируйте свой бэйдж!')
                            $('.prompt-message').show()
                            waitForSocketConnection(socket, JSON.stringify({"code":"0"}))
                            waitForSocketConnection(socket, JSON.stringify({"code":"10", "user-message":"Отсканируйте бэйдж сотрудника!"}))
                            break;
                        case false:
                            $('.prompt-message-text').text('Откройте приложение для аутентификации!')
                             $('.prompt-message').show()
                            break;
                    }
                }
            })


        }
    
    })
}
//////