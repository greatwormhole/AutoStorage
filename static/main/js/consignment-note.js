function promptShow(){
    if ($('#prompt-block-UI').css('display') != 'none'){
    return
    }
    $('#prompt').css({'flex-direction':'column',
                      'border':'1px solid gray',
                      'background-color':'white',
                      'border-radius':'5px 5px 5px 5px'})
    var html = '<div class = "prompt-row " id = "consignment-note-prompt-row">'
    html += '<span class = "margined">Идентификатор:</span>'
    html += '<input type="text" class = "margined" id="input-consignment-note-num">'
    html += '<div id = "save-consignment-note-num" class = "margined"></div>'
    html += '</div>'

    $('#prompt-content').append(html)
    $('#prompt-name').text('Регистрация накладной.')
    $('#prompt-block-UI').show()
    $('#prompt-close').click(function(){
        location.href = home_url
    })
    $('#save-consignment-note-num').click(function(){
        if ($('#input-consignment-note-num').val() == ''){
            if ($('.prompt-message').css('display') != 'none'){
                $('.prompt-message-text').text('Введите идентификатор!')
                return
            }
            $('.prompt-message-text').text('Введите идентификатор!')
            $('.prompt-message').show()
        return
        }
        consignmentNoteId = $('#input-consignment-note-num').val()
        $('#prompt-block-UI').hide()
        $('.prompt-message').hide()
        $('#number').text(consignmentNoteId)
    })
}

function addRow(){
    var html='<tr>'
    html += '<td>'
    html += '</td>'
    html += '<td>'
    html += '</td>'
    html += '<td>'
    html += '</td>'
    html += '<td>'
    html += '</td>'
    html += '<td>'
    html += '</td>'
    html+='</tr>'
    $('#table-body').append(html)
    $('#main-table').scrollTop($('#table-body').height());
}