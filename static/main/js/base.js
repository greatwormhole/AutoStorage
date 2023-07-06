/// authorization logic///
function authorized(){

    $('#login-BU').css('display','none')

}


function nonAuthorized(){

    $('#login-BU').css('display','block')
    $('.content').append('<h2 class="text" id="auth-prompt-text">Необходима авторизация!</h2>')
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
    $('#prompt').css({'width':'250px','flex-direction':'column', 'border':'1px solid black', 'background-color':'white', 'border-radius':'10px 10px 10px 10px'})
    var html = "<div class = 'prompt-body'>"
    for (let i = 0; i<response.length; i++){
        html += ""+response[i].fields.id+""
    }
    html += "</div>"
    $('#prompt-block-UI').show()
}
//////