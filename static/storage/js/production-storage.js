function updateInfo(){
    $.ajax({
        method:"POST",
        async: true,
        url: updateInfoUrl,
        success: function (response){
            createRow(response)
        },
        error: function (response){
            alert('Не удалось обновить страницу! Попробуйте позже!')
        }
    })
}

function createRow(response){
    console.log(response)

}