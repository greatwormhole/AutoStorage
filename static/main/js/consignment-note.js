
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
    html += '<span class = "margined">Идентификатор:</span>'
    html += '<input type="text" class = "margined" id="input-consignment-note-num" maxlength="150">'
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
        window.onbeforeunload = function() {
                return "Накладную придется заполнять заново!";
            };
    })
}
// получение информации GET
function ajaxGet(path){
    var GlobalResponse = {}
    $.ajax({
        method:"GET",
        async: false,
        url: path,
        success: function(response){

            GlobalResponse = response
        },
        error: function(response){
            location.reload
        }
    })
    return GlobalResponse
}
//Доюавление ячейки с товаром
function addRow(){
    var previous = $('.main-table-row')[$('.main-table-row').length-1],
        id = parseInt($(previous).attr('id')) + 1
    if (typeof $(previous).attr('id') === 'undefined'){
        id = 0
    }

    var html='<tr class="main-table-row" id="'+id+'">'
    html += '<td>'
    html += '<span id="'+id+'_articule_span"></span>'
    html += '</td>'
    html += '<td>'
    html += '<select class="js-example-basic-single" id = "'+id+'_select_nomenclature">'
    html += '<option>Добавьте номенклатуру!</option>'
    for (let i=0; i<nomenclature.length;i++){
        html += '<option>'+nomenclature[i].fields.title+'</option>'

    }
    html += '</select>'
    html += '</td>'
    html += '<td>'
    html += '<input type="number"  min="1" class= "input-table" id="'+id+'_count">'
    html += '<span id="'+id+'_unit"></span>'
    html += '</td>'
    html += '<td>'
    html += '<input type="number" min="1" class= "input-table" style="width:18%; border:1px solid gray" id="'+id+'_x">'
    html += '<span> (мм) - </span>'
    html += '<input type="number" min="1" class= "input-table" style="width:18%; border:1px solid gray" id="'+id+'_y">'
    html += '<span> (мм) - </span>'
    html += '<input type="number" min="1" class= "input-table" style="width:18%; border:1px solid gray" id="'+id+'_z">'
    html += '<span> (мм)</span>'
    html += '</td>'
    html += '<td>'
    html += '<button class="print-mark-button">'
    html += '</button>'
    html += '<button class="delete-row-button" id = "'+id+'_delete" onclick="deleteTableRow(this.id)">'
    html += '</button>'
    html += '</td>'

    html+='</tr>'
    $('#table-body').append(html)
    $('#main-table').scrollTop($('#table-body').height());
    $('.js-example-basic-single').attr("lang", "ru").select2({
        language: "ru"
    });
    $('.select2').css({'width':'100%', 'max-width':'100%'})
    $('.select2-selection--single').css({'border':'0px solid', 'background':'none'})

    $('#'+id+'_select_nomenclature').on('change', function(e){
        var id = parseInt(e.target.id.split('_')[0]),
            nom = e.target.value,
            product = {}
        if (nom == 'Добавьте номенклатуру!'){
            $('#'+id+'_articule_span').text('')
            $('#'+id+'_unit').text('')
            return
        }
        for (let i = 0; i<nomenclature.length; i++){
            if (nomenclature[i].fields.title == nom){
               product = nomenclature[i]
            }
        }
        $('#'+id+'_articule_span').text(product.pk)
        $('#'+id+'_count').val(null)
        $('#'+id+'_x').val(null)
        $('#'+id+'_y').val(null)
        $('#'+id+'_z').val(null)
        $('#'+id+'_unit').text(product.fields.units)
        })
    $('.input-table').on('keydown', function(e){
        if (e.keyCode == 69 || e.keyCode == 189){
            return false
        } else {return true}
    })
    }

//delete row

function deleteTableRow(id){
    let isDelete = confirm("Удалить строку номенклатуры?");
    if (isDelete){
        $('#'+id.split("_")[0]).remove()
    }
}

// save note
function saveConsignmentNote(){
    var dataCreates = [],
        data = {}
    let isSave = confirm("Уверены что хотите сохранить накладную?");
    if (isSave){
        for (let i = 0; i<=parseInt($($('.main-table-row')[$('.main-table-row').length-1]).attr('id')); i++){
            var articule = $('#'+i+'_articule_span').text(),
                nomenclature = $('#'+i+'_select_nomenclature').val(),
                count = $('#'+i+'_count').val(),
                unit = $('#'+i+'_unit').text(),
                dimensions = $('#'+i+'_x').val()+'-'+$('#'+i+'_y').val()+'-'+$('#'+i+'_z').val()
            var dataRow = {'articule':articule, 'nomenclature':nomenclature, 'count':count, 'unit':unit, 'dimensions':dimensions}
            console.log(dataRow)
            if(articule == '' || nomenclature == 'Добавьте номенклатуру!' || count == '' || unit == '' || $('#'+i+'_x').val() == '' || $('#'+i+'_y').val()== '' || $('#'+i+'_z').val() == ''){
                return alert('Накладная заполнена не полностью!')
            }
            dataCreates.push(dataRow)

        }
        data = {"worker_id": $('#worker_id').text(),
                "datetime": $('#date').text(),
                "number": $('#number').text(),
                "provider":$('#provider-input').val(),
                "dataCreates":dataCreates
                }
        console.log(data)
        $.ajax({
                method:"POST",
                async: true,
                url: saveConsignmentNoteUrl,
                data:{'data':data},
                success: function (response){
                    window.onbeforeunload = null;
                    location.href = home
                },
                error: function (request){

                }
            })
    }
}