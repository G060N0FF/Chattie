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
                        document.querySelector('#chat-log').innerHTML = displayMessage(s, ['scroll'], ['blue']) + document.querySelector('#chat-log').innerHTML;
                    }
                    else{
                        document.querySelector('#chat-log').innerHTML = displayMessage(s, ['scroll'], []) + document.querySelector('#chat-log').innerHTML;
                    }
                }
                else{
                    if(data[i][0] == username){
                        document.querySelector('#chat-log').innerHTML = displayMessage(s, [], ['blue']) + document.querySelector('#chat-log').innerHTML;
                    }
                    else{
                        document.querySelector('#chat-log').innerHTML = displayMessage(s, [], []) + document.querySelector('#chat-log').innerHTML;
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

function displayMessage(s, ids, color){
    let id_string = "";
    if(ids.length > 0){
        id_string = ids[0];
        for(i=1; i < ids.length; i++){
            id_string += " " + ids[i];
        }
        id_string = " id='" + id_string + "'";
    }
    let color_string = "";
    if(color.length > 0){
        color_string = " style='color:" + color[0] + "' ";
    }
    return "<p" + id_string + color_string + ">" + s + "</p>";
}
