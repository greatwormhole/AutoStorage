
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
        console.log(cellPleasesArray)
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