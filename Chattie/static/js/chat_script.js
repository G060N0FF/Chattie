function preloadMessages(){
    $.ajax({
        url: '/group_messages/load_messages/',
        data: {
            'roomName': roomName,
            'page': page,
        },
        dataType: 'json',
        success: function (data) {
            data = data.messages;
            for(i=0; i<data.length; i++){
                var s =  data[i][0] + ': ' + data[i][1];
                if(i == 0){
                    if(data[i][0] == username){
                        document.querySelector('#chat-log').innerHTML = "<p id='scroll' style='color: blue'>" + s + "</p>" + document.querySelector('#chat-log').innerHTML;
                    }
                    else{
                        document.querySelector('#chat-log').innerHTML = "<p id='scroll'>" + s + "</p>" + document.querySelector('#chat-log').innerHTML;
                    }
                }
                else{
                    if(data[i][0] == username){
                        document.querySelector('#chat-log').innerHTML = "<p style='color: blue'>" + s + "</p>" + document.querySelector('#chat-log').innerHTML;
                    }
                    else{
                        document.querySelector('#chat-log').innerHTML = "<p>" + s + "</p>" + document.querySelector('#chat-log').innerHTML;
                    }
                }
                if(page == 0 || page == 1){
                    var obj = document.querySelector('#chat-log');
                    obj.scrollTop = obj.scrollHeight;
                }
                else{
                    var obj = document.querySelector('#scroll');
                    obj.scrollIntoView();
                }
            }
            page += 1;
        }
    });
}
