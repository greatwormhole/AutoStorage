
function bouncer(arr) {
  return arr.filter( function(v){return !(v !== v);});
}
function dictWrite(dict, key){
    if (typeof dict[key] == 'undefined'){
        dict[key] = 1
    } else {
        dict[key]++
    }
}
function dictWriteNull(dict, key){
     dict[key] = 0
}
function placeCount(dict,id,text){
    Object.keys(dict).forEach((key) => {
        $('#'+key+id).text(text+dict[key])
    })
}
function null2empty(array){
    array.forEach(function(elem, idx){
        var yIdx = idx
        elem.forEach(function(elem,idx){
            if (elem == null){
            delete array[yIdx][idx]
        }
        })

    })
    return array
}
//counter edit
function counter(LockStorage,storageList){
    var $cells = $('.storageCell'),
        globalLockValue = 0,
        globalLockFullValue = 0,
        LockValue = {},
        lockFullValue = {},
        globalFullValue = 0,
        fullValue = {},
        globalEmptyValue = 0,
        emptyValue = {}
    storageList.forEach(function(elem){
        LockValue[elem] = 0
        lockFullValue[elem] = 0
        fullValue[elem] = 0
        emptyValue[elem] = 0
    })
    $cells.each(function(elem){
        var percent = percentUsingColor([96, 255, 68],[255,0,0],$($cells[elem]).css('background-color').replace('rgb(','').replace(')','').split(',')),
            id = $cells[elem].id,
            storageName = id.split('_')[3]
        if ($($cells[elem]).css('background-color') == 'rgb(61, 61, 61)'){
            percent = LockStorage[storageName][id.split('_')[1]+'_'+id.split('_')[0]+'_'+id.split('_')[2]]/100

        }
        if (percent>barerPercentage/100 && typeof LockStorage[storageName][id.split('_')[1]+'_'+id.split('_')[0]+'_'+id.split('_')[2]] == 'undefined'){
            globalFullValue++

            dictWrite(fullValue, storageName)
        } else if (percent<barerPercentage/100 && typeof LockStorage[storageName][id.split('_')[1]+'_'+id.split('_')[0]+'_'+id.split('_')[2]] == 'undefined'){
            globalEmptyValue++
            dictWrite(emptyValue, storageName)
        } else if (percent>barerPercentage/100 && typeof LockStorage[storageName][id.split('_')[1]+'_'+id.split('_')[0]+'_'+id.split('_')[2]] != 'undefined'){
            globalLockFullValue++
            dictWrite(lockFullValue, storageName)
        } else if (percent<barerPercentage/100 && typeof LockStorage[storageName][id.split('_')[1]+'_'+id.split('_')[0]+'_'+id.split('_')[2]] != 'undefined'){
            globalLockValue++
            dictWrite(LockValue, storageName)
        }
    })

    $('#lock-span').text('Заблокировано - '+globalLockValue)
    $('#lock-full-span').text('Занято и заблокировано - '+globalLockFullValue)
    $('#full-span').text('Занято - '+globalFullValue)
    $('#free-span').text('Свободно - '+globalEmptyValue)
    placeCount(fullValue, '-full-span', 'Занято - ')
    placeCount(emptyValue, '-free-span', 'Свободно - ')
    placeCount(LockValue,'-lock-span','Заблокировано - ')
    placeCount(lockFullValue, '-lock-full-span','Занято и заблокировано - ')
}
//percentUsingColor
function percentUsingColor(first, second, present){
  let firstColor = first[0];
  let secondColor = second[0];
  let presentColor = parseInt(present[0]);
  if (presentColor>255){
        return 1
    }
  var result = (presentColor-firstColor)/(secondColor-firstColor)
  return result;
}
//color calculate
function calculate(first, second, percentage) {
    if (percentage>1){
        return second
    }
  let result = {};
  Object.keys(first).forEach((key) => {
    let start = first[key];
    let end = second[key];
    let offset = (start - end) * percentage;
    if(offset >= 0) {
      Math.abs(offset);
    }
    result[key] = (start - offset);
  });
  return result;
}
function zeroCount(arr){
    var count = 0
    for (let i=0; i<arr.length; i++){
        if (arr[i] == 0){
        count++
        }
    }

    return 1-count/arr.length
}

function zeroCountNum(arr){
    var count = 0
    for (let i=0; i<arr.length; i++){
        if (arr[i] == 0){
        count++
        }
    }
    return count
}
function appendNumbers(count, storageName, type){
    for (let i = 0; i<count; i++){
        switch (type){
            case 'row':
                $('#'+storageName+'-row-numbers').append('<span>'+i+'</span>')
                break
            case 'column':
                $('#'+storageName+'-column-numbers').append('<span>'+i+'</span>')
                break
        }
    }
}
//build storage plan
function buildStorages(storageList,LockStorage,storageInfo){
    var cellPleasesArray = [],
        cells = []

    for (let i=0; i<storageList.length; i++){
        var storageCell = null2empty(storageInfo[storageList[i]]),
            rowNumber,
            storageName=storageList[i]
        cellPleasesArray.push(storageCell)
        cellInformation = cellPleasesArray
        var storageDiv = $('#' + storageList[i]),
            screenWidth = parseInt($('#view-space').css('width')),
            height = storageCell.map((elem) => elem[0][0][1]).reduce((partialSum, a) => partialSum + a, 0)*Math.max.apply(Math,bouncer(storageCell.map((elem) => Math.max.apply(Math, elem.map((elem) => elem.length))))),
            scaleY = screenWidth * 1 / height
            columnCount = storageCell.length
            rowCount = Math.max.apply(Math, storageCell.map((elem)=>elem.length))
        appendNumbers(columnCount, storageName, 'column')
        appendNumbers(rowCount, storageName, 'row')
        storageCell.forEach(function(row,idx){
            var htmlRow = '<div class = "storageRow" id = "'+idx+'_st_row_'+storageName+'">',
                    rowIdx = idx
                htmlRow += '</div>'
                $(storageDiv).append(htmlRow)
            var scaleXList = [],
                countLayer = [],
                planLayer = [],
                lengthList = []
            for (let i=0; i<row.length;i++){
                if(typeof row[i] == "undefined"){
                    planLayer.map((elem)=>elem.push(0))
                    continue
                }

                for (let j=0; j<row[i].length; j++){
                    if (typeof countLayer[j] == 'undefined'){
                        countLayer[j] = 1
                        scaleXList[j] = parseInt(row[i][j][0])
                        planLayer.push([1])
                    } else {
                        countLayer[j] += 1
                        scaleXList[j] += parseInt(row[i][j][0])
                        planLayer[j].push(1)
                    }
                }
            }

            lengthList = scaleXList

            scaleXList = scaleXList.map((length, idx) => (screenWidth-planLayer[idx].length*8)/(length/(zeroCount(planLayer[idx]))))

            row.forEach(function(column, idx){
                var columnIdx = idx
                column.forEach(function(layer,idx){

                    if ($('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).length==0){
                    var htmlLayer = '<div id="'+idx+'_'+rowIdx+'_st_layer_'+storageName+'" class="storageLayer">'
                    htmlLayer += '</div>'
                    $('#'+rowIdx+'_st_row_'+storageName).append(htmlLayer)
                    }


                    var color = calculate([96, 255, 68],[255,0,0],storageCell[rowIdx][columnIdx][idx][0][3]/100),
                        percent = storageCell[rowIdx][columnIdx][idx][0][3]
                    color = 'rgb('+color[0]+','+color[1]+','+color[2]+')'

                    if (typeof LockStorage[storageName][columnIdx+'_'+rowIdx+'_'+idx]!='undefined'){
                        color = 'rgb(61,61, 61);'
                    }
                    if (scaleXList[idx]>maxScale){
                        var html = '<div class = "storageCell" id = "'+rowIdx+'_'+columnIdx+'_'+idx+'_'+storageName+'_cell" style = "width:'+layer[0][0]*maxScale+'px; height:'+layer[0][1]*maxScale+'px; background:'+color+'">'+idx
                        html += '</div>'
                        $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                    } else{
                        var html = '<div class = "storageCell" id = "'+rowIdx+'_'+columnIdx+'_'+idx+'_'+storageName+'_cell" style = "width:'+layer[0][0]*scaleXList[idx]+'px; height:'+layer[0][1]*scaleXList[idx]+'px; background:'+color+'">'+idx
                        html += '</div>'
                        $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                    }
                    var i = columnIdx
                    while (planLayer[idx][i+1] == 0){
                        var html = '<div class = "space" style = "width:'+parseFloat((lengthList[idx]/(zeroCount(planLayer[idx]))-lengthList[idx])*scaleXList[idx]/(zeroCountNum(planLayer[idx]))+6)+'px;max-width:'+parseFloat(parseFloat($('.storageCell').css('width'))+6)+'px">'
                        html += '</div>'
                        $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                        i++
                    }
                })
            })
        })
        counter(LockStorage,storageList)
       storageMargin(storageCell,storageName,false)
    }
    //информация о коробках в ячейке
    $('.storageCell').on('click', function(event){
        var id = event.target.id,
            data = getCellContent(id),
            parentWidth = parseInt($(event.target).parent().css('width')),
            localX = event.target.offsetLeft
        console.log(data)
        const localY = event.target.offsetTop+parseInt($(event.target).css('height'))
        if (parentWidth*0.25>localX ){
            localX = event.target.offsetLeft
        } else if(parentWidth*0.25<localX && parentWidth*0.75>localX){
            console.log('ds')
            localX = event.target.offsetLeft - 125 + parseInt($(event.target).css('width'))/2
        } else if(parentWidth*0.75<localX){
            localX = event.target.offsetLeft - 250 + parseInt($(event.target).css('width'))

        }
        if (typeof $('.create-info').attr('id') != 'undefined'){
            $('#'+$('.create-info').attr('id').replace('_visualizeInfo','')).css({'border':'1px solid gray'})
        }
        $('.create-info').remove()
        $(event.target).css({'border':'3px solid gold'})

        var html = '<div id = "'+id+'_visualizeInfo" class="create-info" style="left:'+localX+'px;top:'+localY+'px">'
        html+='<h6>Список номенклатуры в ячейке:</h6>'
        html+='<div class="scroll-table">'
        html+='<table>'
        html+='<thead>'
        html+='<tr>'
        html+='<th>Номенклатура'
        html+='</th>'
        html+='<th>Кол-во'
        html+='</th>'
        html+='</tr>'
        html+='</thead>'
        html+='<tbody>'
        if(data.length == 0){
            html+='<tr>'
            html+='<td style="width:100%">Пустая ячейка'
            html+='</td>'
            html+='<td style="width:100%">Пустая ячейка'
            html+='</td>'
            html+='</tr>'
        }else{
        for (let i=0;i<data.length;i++){
            html+='<tr>'
            html+='<td title="'+data[i].title+'">'+data[i].title
            html+='</td>'
            html+='<td>'+data[i].amount+data[i].units
            html+='</td>'
            html+='</tr>'

        }
        }
        html+='</tbody>'
        html+='</table>'
        html+='</div>'
        html+='</div>'

        if ($('#'+id+'_visualizeInfo').length != 0){
            return
        }
        $('#'+id.split('_')[3]).append(html)
    })
}
function storageMargin(storageCell,storageName, isUnMargin){
    storageCell.forEach(function(row,idx){
            var rowIdx = idx
            row.forEach(function(column,idx){
                column.forEach(function(layer,idx){
                    if(idx!=0){
                        var prevRowHeight = parseFloat($('#'+parseInt(idx-1)+'_'+rowIdx+'_st_layer_'+storageName).css('height'))
                        if (typeof prevRowHeight != 'undefined'){
                            if(!isUnMargin){
                                $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).css({'margin-top':'-'+prevRowHeight*percentForRow+'px','margin-left': idx*marginLeft+'px'})
                            } else{
                                $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).css({'margin-top':'0px','margin-left': '0px'})
                            }
                        }
                    }
                })
            })
        })
}

function getCells(id){
    var responseCell = []
    $.ajax({
        method:"GET",
        async:false,
        url: getCellsUrl,
        data: {"data":id},
        success: function(response){
            responseCell = response
        }
    })
    return responseCell
}


function canvasDraw(){
    var canvas = document.getElementById('legend-canvas');
  if (canvas.getContext){
    var ctx = canvas.getContext('2d');
    ctx.lineWidth = 3;
    ctx.beginPath()
    ctx.moveTo(0,0)
    ctx.lineTo(0,20)
    ctx.stroke()
    ctx.beginPath()
    ctx.moveTo(350,0)
    ctx.lineTo(350,20)
    ctx.stroke()

    //скобки
    ctx.lineWidth = 1;
     ctx.beginPath()
    ctx.moveTo(0,10)
    ctx.lineTo(350,10)
    ctx.stroke()
    ctx.beginPath()
    ctx.moveTo(175,10)
    ctx.lineTo(175,0)
    ctx.stroke()
  }
}

function OCStorage(id){
    var storage=id.replace('_OC',''),
        storageNameList = storageList
    if ($('#'+id).css('transform') == 'none' || $('#'+id).css('transform') == 'matrix(1, 0, 0, 1, 0, 0)'){
        $('#'+storage).children().css({'margin-top':'0px','margin-bottom':'0px'})
        storageMargin(cellInformation[storageNameList.indexOf(storage)],storage,false)
        $('#'+id).css({'transform':'rotate(180deg)'})
        return
    }
    storageMargin(cellInformation[storageNameList.indexOf(storage)],storage,true)
    $('#'+id).css({'transform':'rotate(0deg)'})
}

function getStorageInfo(url){
    var cellFullnessResponse
    $.ajax({
        method:"GET",
        async:false,
        url:url,
        success: function (response){
            cellFullnessResponse = response
        },
        error: function(response){
            alert('Загразить информацию о заполненности склада не удалось, перезагрузите страницу!')
        }
    })
    return cellFullnessResponse
}


function processMessage(message,storageList){
    LockStorage = getStorageInfo(storageLockUrl)
    message.forEach(function(elem){
        var percent = elem['fullness'],
            origin_percent = elem['origin_fullness']
        if (typeof percent != 'undefined'){
            var color = calculate([96, 255, 68],[255,0,0], percent/100)
            if (elem['is_blocked'] == true){
                color = [61,61,61]
            }
            $('#'+elem['y_coord']+'_'+elem['x_coord']+'_'+elem['z_coord']+'_'+elem['storage_name']+'_cell').css({'background':'rgb('+color[0]+','+color[1]+','+color[2]+')'})
        }
        if (typeof origin_percent != 'undefined'){
            var color = calculate([96, 255, 68],[255,0,0], origin_percent/100)
            if (elem['is_blocked_origin'] == true){
                color = [61,61,61]

            }
            $('#'+elem['y_coord_origin_cell']+'_'+elem['x_coord_origin_cell']+'_'+elem['z_coord_origin_cell']+'_'+elem['storage_name_origin']+'_cell').css({'background':'rgb('+color[0]+','+color[1]+','+color[2]+')'})
        }
    })
    counter(LockStorage,storageList)
}

function getCellContent(cell){
    var x = cell.split('_')[1],
        y = cell.split('_')[0],
        z = cell.split('_')[2],
        storageName = cell.split('_')[3],
        responseCreates = []
    $.ajax({
        method:"GET",
        async:false,
        url: getCellContentUrl,
        data: {"x":x, "y":y, "z":z, "name":storageName},
        success: function(response){
            responseCreates = response
        }
    })
    return responseCreates
}

//settings open
function viewSettings(){
    if ($('#prompt-block-UI').css('display') != 'none'){
        return
    }
    if ($('#prompt-name').text() == 'Настройки'){
        return $('#prompt-block-UI').show()
    }
    $('#prompt').css({'flex-direction':'column',
                      'border':'1px solid gray',
                      'background-color':'white',
                      'border-radius':'5px 5px 5px 5px'})
    var html = '<div class = "prompt-row " id = "consignment-note-prompt-row">'
    html += '<h5 class = "margined settings-title" style="margin-bottom: 0px;">Параметры отображения</h5>'
    html += '</div>'
    html += '<div class = "prompt-row " id = "consignment-note-prompt-row">'
    html += '<h6>Отображение складов</h6>'
    html += '</div>'
    html += '<div class = "prompt-row " id = "consignment-note-prompt-row">'
    html += '<div class = "storage-visualize-settings">'
    for (let i =0 ; i<storageList.length;i++){
        html += '<div>'
        html += '<input type = "checkbox" id = "'+storageList[i]+'_settings_check" class="settings-check" checked>'
        html += '<label for="'+storageList[i]+'_settings_check">'+storageList[i]+'</label>'
        html += '</div>'
    }
    html += '</div>'
    html += '</div>'

    $('#prompt-content').append(html)
    $('#prompt-name').text('Настройки')
    $('#prompt-block-UI').show()
    $('.settings-check').prop('checked')
    $('#prompt-close').attr('onclick', 'hidePromptVis()')
    $('.settings-check').on('change', function(event){
        var value = $(event.target).is(':checked'),
            id = event.target.id
        if (value){
            $('#'+id.replace('_settings_check','')+'-container').css({'display':'flex'})
            return
        }
        $('#'+id.replace('_settings_check','')+'-container').css({'display':'none'})
    })
}

function hidePromptVis(){
    $('#prompt-block-UI').hide()
}