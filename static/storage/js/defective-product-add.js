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
function saveDefProdNote(){
    var dataItems = [],
        data = {}
    let isSave = confirm("Уверены что хотите сохранить акт выбраковки?");
    if (isSave){
        if (typeof $($('.main-table-row')[$('.main-table-row').length-1]).attr('id') == 'undefined'){
            return alert('Накладная заполнена не полностью!')
        }
        for (let i = 0; i<=parseInt($($('.main-table-row')[$('.main-table-row').length-1]).attr('id')); i++){
            var articule = $('#'+i+'_articule_span').text(),
                nomenclature = $('#'+i+'_select_nomenclature').val(),
                count = $('#'+i+'_count').val(),
                unit = $('#'+i+'_unit').text()
            var dataRow = {'articule':articule, 'nomenclature':nomenclature, 'count':count, 'unit':unit}
            console.log($('#'+i+'_articule_span').length)
            if(articule == '' || nomenclature == 'Добавьте номенклатуру!' || count == '' || unit == ''){
                return alert('Акт заполнен не полностью!')
            }
            dataItems.push(dataRow)
        }
        data = {"worker_id": $('#worker_id').text(),
                "datetime": $('#date').text(),
                "dataItems":dataItems
                }
        $.ajax({
                method:"POST",
                async: true,
                url: defectiveProdSaveActUrl,
                data: JSON.stringify({'data': data}),
                success: function (response){
                    window.onbeforeunload = null;
                    location.reload()
                },
                error: function (request){
                    alert('Ошибка при сохранении, попробуйте позже!')
                }
        })
    }
}