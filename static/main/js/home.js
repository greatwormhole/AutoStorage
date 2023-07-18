///redirect
var pathList = {
    'consignment-note': consignmentNote
}
function redirect(idList){

    for (i=0; i<idList.length; i++){
        $('#'+idList[i]).on('click', function(){
            location.href = pathList[this.id]
        })
    }
}
/// visualization using rights
function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}
/// authorization button logic///
$(document).ready(function(){
    var rights = JSON.parse(getCookie('AccessKey').replace(/\\054/g, ','))
    if (JSON.parse(rights)["storage_right"] == false){
        var html = "<div class = 'rights'>"
        html += "<h2 class = 'text'>Склад</h2>"
        html += "<button class = 'storage' id = 'consignment-note'>"
        html += "<span class = 'text' >Создать накладную.</span>"
        html += "</button>"
        html += "<button class = 'storage' id = 'broken-parts-in'>"
        html += "<span class = 'text'>Внести бракованные изделия.</span>"
        html += "</button>"
        html += "<button class = 'storage' id = 'visualise-storage'>"
        html += "<span class = 'text'>Визуализация склада.</span>"
        html += "</button>"
        html += "<button class = 'storage' id = 'parts-in-factory'>"
        html += "<span class = 'text'>Материальные ценности на производстве.</span>"
        html += "</button>"
        html += "<button class = 'storage' id = 'search'>"
        html += "<span class = 'text'>Навигация по складу.</span>"
        html += "</button>"
        html += "</div>"
        $('#button-panel').append(html)

        redirect(['consignment-note'])
    }
    if (JSON.parse(rights)["plan_right"] == false){
        var html = "<div class = 'rights'>"
        html += "<h2 class = 'text'>Планирование</h2>"
        html += "<button class = 'plan' id = 'month-plan'>"
        html += "<span class = 'text'>Задать план на месяц.</span>"
        html += "</button>"
        html += "<button class = 'plan' id = 'shift-plan'>"
        html += "<span class = 'text'>Задать план на смену.</span>"
        html += "</button>"
        html += "<button class = 'plan' id = 'real-prod'>"
        html += "<span class = 'text'>Фактическое производство.</span>"
        html += "</button>"
        html += "</div>"
        $('#button-panel').append(html)
    }
    if (JSON.parse(rights)["quality_control_right"] == false){
        var html = "<div class = 'rights'>"
        html += "<h2 class = 'text'>Отдел качества</h2>"
        html += "<button class = 'quality'>"
        html += "<div class = 'consignment-note-sign' id = 'flaw-send'></div>"
        html += "<span class = 'text' >Внести бракованные изделия.</span>"
        html += "</button>"
        html += "<button class = 'quality'>"
        html += "<div class = 'consignment-note-sign' id = 'flaw-decision'></div>"
        html += "<span class = 'text'>Вынести вердикт по браку.</span>"
        html += "</button>"
        html += "</div>"
        $('#button-panel').append(html)
    }

})