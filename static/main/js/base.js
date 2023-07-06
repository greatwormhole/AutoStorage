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
        async: false,
        url: "{% url 'settings' %}",
        data:{'action':action},

    })
}