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
    return 1+count/arr.length
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
            rowNumber
        for (let j = 0; j<cells.length; j++){
            rowNumber = cells[j].fields.y_cell_coord
            if (storageCell[rowNumber] == null){
                storageCell[rowNumber] = []
                storageCell[rowNumber][cells[j].fields.x_cell_coord] = []
                storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.x_cell_size, cells[j].fields.y_cell_size, cells[j].fields.z_cell_size]
            } else {
                if (storageCell[rowNumber][cells[j].fields.x_cell_coord] == null){
                    storageCell[rowNumber][cells[j].fields.x_cell_coord] = []
                    storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.x_cell_size, cells[j].fields.y_cell_size, cells[j].fields.z_cell_size]

                } else {
                    storageCell[rowNumber][cells[j].fields.x_cell_coord][cells[j].fields.z_cell_coord]=[cells[j].fields.x_cell_size, cells[j].fields.y_cell_size, cells[j].fields.z_cell_size]
                }
            }
        }
        cellPleasesArray.push(storageCell)

        var storageDiv = $('#' + storageList[i]),
            screenWidth = parseInt($('#view-space').css('width')),
            height = storageCell.map((elem) => elem[0][0][1]).reduce((partialSum, a) => partialSum + a, 0)*Math.max.apply(Math,bouncer(storageCell.map((elem) => Math.max.apply(Math, elem.map((elem) => elem.length))))),
            scaleY = screenWidth * 1 / height

        storageCell.forEach(function(row,idx){
            var htmlRow = '<div class = "storageRow" id = "'+idx+'_st_row">',
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
            scaleXList = scaleXList.map((length, idx) => (screenWidth-countLayer[idx]*8)/(length*zeroCount(planLayer[idx])))
            row.forEach(function(column, idx){
                var columnIdx = idx
                column.forEach(function(layer,idx){
                    if ($('#'+idx+'_'+rowIdx+'_st_layer').length==0){
                    var htmlLayer = '<div id="'+idx+'_'+rowIdx+'_st_layer" class="storageLayer">'
                    htmlLayer += '</div>'
                    $('#'+rowIdx+'_st_row').append(htmlLayer)
                    }
                    var i = columnIdx
                    while (planLayer[idx][i+1] == 0){

                        html = '<div class = "space" style = "width:'+parseFloat(lengthList[idx]*(zeroCount(planLayer[idx])-1)*scaleXList[idx]/(zeroCountNum(planLayer[idx]))-2)+'px;">'
                        html += '</div>'
                        $('#'+idx+'_'+rowIdx+'_st_layer').append(html)
                        i++
                    }
                    var html = '<div class = "storageCell" style = "width:'+layer[0]*scaleXList[idx]+'px; height:'+layer[1]*scaleY+'px">'
                    html += '</div>'

                    $('#'+idx+'_'+rowIdx+'_st_layer').append(html)
                })
            })
        })



    }

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