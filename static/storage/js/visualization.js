function bouncer(arr) {
  return arr.filter( function(v){return !(v !== v);});
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
//build storage plan
function buildStorages(storageList){
    var storageList = JSON.parse(storageList.replaceAll('&#x27;','"')),
        cellPleasesArray = [],
        cells = []
    for (let i=0; i<storageList.length; i++){
        cells = getCells(storageList[i])
        var storageCell = [],
            rowNumber,
            storageName=storageList[i]
        for (let j = 0; j<cells.length; j++){
            rowNumber = cells[j].fields.y_cell_coord
            if (storageCell[rowNumber] == null){
                storageCell[rowNumber] = []
                storageCell[rowNumber][cells[j].fields.x_cell_coord] = []
                storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.visualization_x, cells[j].fields.visualization_y, cells[j].fields.z_cell_size]
            } else {
                if (storageCell[rowNumber][cells[j].fields.x_cell_coord] == null){
                    storageCell[rowNumber][cells[j].fields.x_cell_coord] = []
                    storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.visualization_x, cells[j].fields.visualization_y, cells[j].fields.z_cell_size]

                } else {
                    storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.visualization_x, cells[j].fields.visualization_y, cells[j].fields.z_cell_size]
                }
            }
        }
        cellPleasesArray.push(storageCell)
        cellInformation = cellPleasesArray
        var storageDiv = $('#' + storageList[i]),
            screenWidth = parseInt($('#view-space').css('width')),
            height = storageCell.map((elem) => elem[0][0][1]).reduce((partialSum, a) => partialSum + a, 0)*Math.max.apply(Math,bouncer(storageCell.map((elem) => Math.max.apply(Math, elem.map((elem) => elem.length))))),
            scaleY = screenWidth * 1 / height

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
                        scaleXList[j] = row[i][j][0]
                        planLayer.push([1])
                    } else {
                        countLayer[j] += 1
                        scaleXList[j] += row[i][j][0]
                        planLayer[j].push(1)
                    }
                }
            }

            lengthList = scaleXList
            scaleXList = scaleXList.map((length, idx) => (screenWidth-planLayer[idx].length*8)/(length/(zeroCount(planLayer[idx]))))
            console.log(scaleXList)
            row.forEach(function(column, idx){
                var columnIdx = idx
                column.forEach(function(layer,idx){
                    if ($('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).length==0){
                    var htmlLayer = '<div id="'+idx+'_'+rowIdx+'_st_layer_'+storageName+'" class="storageLayer">'
                    htmlLayer += '</div>'
                    $('#'+rowIdx+'_st_row_'+storageName).append(htmlLayer)
                    }
                    var i = columnIdx


                    if (scaleXList[idx]>maxScale){
                        var html = '<div class = "storageCell" style = "width:'+layer[0]*maxScale+'px; height:'+layer[1]*maxScale+'px">'
                    html += '</div>'

                    $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                    } else{
                    var html = '<div class = "storageCell" style = "width:'+layer[0]*scaleXList[idx]+'px; height:'+layer[1]*scaleXList[idx]+'px">'
                    html += '</div>'

                    $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                    }
                    while (planLayer[idx][i+1] == 0){
                        console.log(lengthList[idx]/(zeroCount(planLayer[idx]))-lengthList[idx])
                        var html = '<div class = "space" style = "width:'+parseFloat((lengthList[idx]/(zeroCount(planLayer[idx]))-lengthList[idx])*scaleXList[idx]/(zeroCountNum(planLayer[idx]))+6)+'px;max-width:'+parseFloat(parseFloat($('.storageCell').css('width'))+6)+'px">'
                        html += '</div>'


                        $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).append(html)
                        i++
                    }
                })
            })
        })
       storageMargin(storageCell,storageName,false)


    }

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
                                $('#'+idx+'_'+rowIdx+'_st_layer_'+storageName).css({'margin-top':'-'+prevRowHeight*0.8+'px','margin-left': idx*marginLeft+'px'})
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
        storageNameList = JSON.parse(storageList.replaceAll('&#x27;','"'))
    if ($('#'+id).css('transform') == 'none' || $('#'+id).css('transform') == 'matrix(1, 0, 0, 1, 0, 0)'){
        $('#'+storage).children().css({'margin-top':'0px','margin-bottom':'0px'})
        storageMargin(cellInformation[storageNameList.indexOf(storage)],storage,false)
        $('#'+id).css({'transform':'rotate(180deg)'})
        return
    }
    storageMargin(cellInformation[storageNameList.indexOf(storage)],storage,true)
    $('#'+id).css({'transform':'rotate(0deg)'})
}