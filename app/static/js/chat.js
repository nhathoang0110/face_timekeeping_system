
            $(document).ready(function(){
             var socket;
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat1');
                socket.on('connect', function() {
                    socket.emit('joined', {});
                });
//                socket.on('status', function(data) {
//                    $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
//                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
//                });
                socket.on('message', function(data) {
                    console.log('aaaa')
                    console.log(data.conver_id)
                    console.log($('#send_button').attr('conversation_id'))
                    if (data.conver_id == $('#send_button').attr('conversation_id')){
                        $('#chats').append(' <div class="chat chat-left">'
                                                    +'   <div class="chat-avatar">'
                                                    +'       <a href="#" class="avatar">'
                                                    +'           <img  src="/static/'+ data.sender_avatar+'" class="img-fluid rounded-circle">'
                                                    +'       </a>'
                                                    +'   </div>'
                                                    +'   <div class="chat-body">'
                                                    +'       <div class="chat-bubble">'
                                                    +'           <div class="chat-content">'
                                                    +'               <p>'+data.msg+'</p>'
                                                    +'               <span class="chat-time">'+data.time+'</span>'
                                                    +'           </div>'
                                                    +'       </div>'
                                                    +'   </div>'
                                                    +'</div> ')
//                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                    }
                });

                $('#send_button').on('click', function () {
                    text = $('#input_mess').val();
                    console.log(text)
                        if (text != ''){
                            $('#input_mess').val('');
                            conver_id = parseInt($('#send_button').attr('conversation_id'))
                       socket.emit('text', {msg: text, conver_id: conver_id});
                        date = new Date()
                        $('#chats').append(' <div class="chat chat-right">'
                                                  +'  <div class="chat-body">'
                                                  +'      <div class="chat-bubble">'
                                                  +'          <div class="chat-content">'
                                                  +'              <p>'+text+'</p>'
                                                  +'              <span class="chat-time">'+date.getHours()+
                                                  ":"+date.getMinutes()+ ' , '
                                                  +date.getDate()+
                                                  "/"+(date.getMonth()+1)+'</span>'
                                                  +'          </div>'
                                                  +'      </div>'
                                                  +'  </div>'
                                                +'</div>')

                            //  $('#chats').scrollTop($('#chats')[0].scrollHeight);
                        }

                });

            });

// function addMess(){
//     text = $('#input_mess').val();
//                     console.log(text)
//                         if (text != ''){
//                             $('#input_mess').val('');
// //                        socket.emit('text', {msg: text});

//                         $('#chats').append(' <div class="chat chat-right">'
//                                                   +'  <div class="chat-body">'
//                                                   +'      <div class="chat-bubble">'
//                                                   +'          <div class="chat-content">'
//                                                   +'              <p>'+text+'</p>'
//                                                   +'              <span class="chat-time">8:30 am</span>'
//                                                   +'          </div>'
//                                                   +'      </div>'
//                                                   +'  </div>'
//                                                 +'</div>')

//                             //  $('#chats').scrollTop($('#chats')[0].scrollHeight);
//                         }
// }


function getChatView(conversation_id){
    console.log(conversation_id)

    var form_data = new FormData()
    form_data.append('conver_id' , parseInt(conversation_id))

    $.ajax({
        url: '/chat_view', // point to server-side URL
        dataType: 'json', // what to expect back from server
        contentType: false,
        processData: false,
        data: form_data,
        type: 'POST',
        success: function (response) {
            console.log(response.status)
            
            cur_user = response.current_user_id
            receiver = response.receiver
            mess = response.messages

            text = ''
            console.log(mess)
            $('#img_header').attr('src', '/static/' + receiver.avatar)
            $('#name_header').text(receiver.name)
            $('#send_button').attr('conversation_id', receiver.id)

            
            for (i = 0; i< mess.length; i++){
                // var date = new Date(mess[i].time_create)
                if (mess[i].sender_id == cur_user){
                    text += '<div class="chat chat-right">'
                            +'    <div class="chat-body">'
                            +'      <div class="chat-bubble">'
                            +'          <div class="chat-content">'
                            +'              <p>'+mess[i].content+'</p>'
                            +'              <span class="chat-time">'+mess[i].time_create+'</span>'
                            +'          </div>'
                            +'      </div>'
                            +'  </div>'
                            +'</div>'
                }
                else{
                    text += '<div class="chat chat-left">'
                            +'    <div class="chat-avatar">'
                            +'      <a href="#" class="avatar">'
                            +'          <img alt="'+ receiver.name+'" src="/static/'+receiver.avatar+'" class="img-fluid rounded-circle">'
                            +'      </a>'
                            +'  </div>'
                            +'  <div class="chat-body">'
                            +'      <div class="chat-bubble">'
                            +'          <div class="chat-content">'
                            +'              <p>'+mess[i].content+'</p>'
                            +'              <span class="chat-time">'+mess[i].time_create+'</span>'
                            +'          </div>'
                            +'      </div>'
                            +'  </div>'
                            +'</div>'
                }
            }


            $('.chats').html(text)
            
        },
        error: function (response) {
            console.log(response.status)
            alert(response.message)
        }
    });
}