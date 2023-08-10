function setWSHandler (ws){
    $(ws).on('message', function(event){
        var data = JSON.parse(event.originalEvent.data),
           message = JSON.parse(data['message']);
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
                var connection_data = message.data
                $.ajax({
                    method:"GET",
                    async: true,
                    url: THDSelect,
                    data:{"ip": connection_data.ip},
                    
                    })

                break;
            case 111:
                var connection_data = message.data
                console.log(connection_data)

                $.ajax({
                     method:"POST",
                     async: true,
                     url: login_url,
                     data:{'id':connection_data.id, "ip": connection_data.ip},
                     success: function (response){
                        ws.send(JSON.stringify({"code":"1000", "user-message":"Авторизация прошла успешно!"}))
                        location.reload()
                     },
                     error: function (response){
                        $.ajax({
                            method:"POST",
                            async: true,
                            url: logout_url,
                            data:{"ip": connection_data.ip},
                            success: function (response){
                                ws.send(JSON.stringify({"code":"1001", "user-message":"Ошибка авторизации, попробуйте снова!"}))
                                $('.prompt-message').hide()
                                promptHide()
                            }
                            })
                     }
                })
                break;
        }
    })
}