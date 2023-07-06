/// authorization logic///
function authorized(){

    $('#login-BU').css('display','none')

}


function nonAuthorized(){

    $('#login-BU').css('display','block')
    $('.content').append('<h2 class="text" id="auth-prompt-text">Необходима авторизация!</h2>')
}

///prompt logic///
function promptHide(obj){
    $(obj).parent().parent().parent().hide()
    $('#prompt-content').children().remove()
}

/// choose THD screen///
function chooseTHD(){
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
        html += "<div class = 'prompt-cell'><span>"+response[i].fields.THD_number+"</span></div>"
        html += "<div class = 'prompt-cell'><span>"+response[i].fields.ip+"</span></div>"
        if (!response[i].fields.is_using){
            html += "<div class = 'prompt-cell'><button class = 'positive'>Выбрать</button></div>"
        } else{
            html += "<div class = 'prompt-cell'><button disabled>В работе</button></div>"
        }
        html += "</div>"
    }

    $('#prompt-content').append(html)
    $('.prompt-cell').css({'flex-basis':'33.33%'})
    $('#prompt-name').text('Список доступных ТСД.')
    $('#prompt-block-UI').show()
}


//////