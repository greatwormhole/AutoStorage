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

    var html = ''
    nomenclature = response
    for (let i=0; i<response.length; i++){
        html += '<tr style="border-bottom:1px solid #9a9a9a;">'
        html += '<td>'+response[i].pk+'</td>'
        html += '<td>'+response[i].fields.amount+' '+response[i].fields.units+'</td>'
        html += '</tr>'

    }
    $('#storage-list').append(html)
}


//search

//start
function promptShow(){
    if ($('#prompt-block-UI').css('display') != 'none'){
    return
    }

    $('#prompt').css({'flex-direction':'column',
                      'border':'1px solid gray',
                      'background-color':'white',
                      'border-radius':'5px 5px 5px 5px'})
    var html = '<div class = "prompt-row " id = "consignment-note-prompt-row">'

    html += '<select class="js-example-basic-single">'
    html += '<option>Выберите номенклатуру!</option>'
    for (let i=0; i<nomenclature.length;i++){
        html += '<option>'+nomenclature[i].pk+'</option>'

    }
    html += '</select>'
    html += '<span style="margin-left:auto;">Кол-во:</span>'
    html += '<span style="margin-left:5px; margin-right:auto;" id="prod-count"></span>'
    html += '</div>'

    $('#prompt-content').append(html)
    $('#prompt-name').text('Поиск.')
    $('.js-example-basic-single').attr("lang", "ru").select2({
        language: "ru"
    });
    $('.select2').css({'width':'50%', 'max-width':'50%'})
    $('#prompt-block-UI').show()
    $('#prompt-close').click(function(){
        $('#prompt-block-UI').hide()
    })
    $('.js-example-basic-single').on('change', function(e){
        if (e.target.value == 'Выберите номенклатуру!'){
            $('#prod-count').text('')
            return
        }
        $('#prod-count').text(nomenclature.find(function(element){
                console.log(e.target.value)
                if (element.pk == e.target.value){
                    return element
                }}).fields.amount + ' ' + nomenclature.find(function(element){
                if (element.pk == e.target.value){
                    return element
                }}).fields.units)
        })
    }