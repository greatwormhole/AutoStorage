function setWSHandler (ws){
    $(ws).on('message', function(event){
        var data = JSON.parse(event.originalEvent.data),
           message = JSON.parse(data['message']);
        console.log(message)
        switch (message.code){
            case 11:
                switch($('.prompt-message-text').text()){
                    case 'Откройте приложение для аутентификации!':
                        $('.prompt-message-text').text('Отсканируйте свой бэйдж!')
                        ws.send(JSON.stringify({"code":"10", "user-message":"Отсканируйте бэйдж сотрудника!"}))
                        break;

                }
                break;
            case 101:
                $('.prompt-message-text').text('Переподключите ТСД!')
                break;
            case 111:
                $.ajax({
                     method:"POST",
                     async: true,
                     url: login,
                     data:{'id':message.id},
                     success: function (response){
                        this.location.reload
                     }
                })
                break;
        }
    })
}