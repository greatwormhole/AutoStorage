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
        $('#'+id+'_unit').text(product.fields.units)
        })
    $('.input-table').on('keydown', function(e){
        if (e.keyCode == 69 || e.keyCode == 189){
            return false
        } else {return true}
    })
    }
