function setWSHandler (ws){
    $(ws).on('message', function(event){
        var data = JSON.parse(event.originalEvent.data),
           message = JSON.parse(data['message']);
        console.log(message)
        switch (message.code){
            case 11:
                switch($('.prompt-message-text').text()){
                    case 'Откройте приложение для аутентификации!':
                        ///ws.send()
                        $('.prompt-message-text').text('Отсканируйте свой бэйдж!')
                        break;

                }
            break;
        case 101:
            $('.prompt-message-text').text('Переподключите ТСД!')
        break;
    }
})
}