
            $(document).ready(function(){
                var socket;
                socket = io.connect('http://' + document.domain + ':' + location.port + '/chat1');
                socket.on('connect', function() {
                    socket.emit('joined', {});
                });
                socket.on('status', function(data) {
                    $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
                    $('#chat').scrollTop($('#chat')[0].scrollHeight);
                });
                socket.on('message', function(data) {
                    $('#chats').append(' <div class="chat chat-left">'
                                                 +'   <div class="chat-avatar">'
                                                 +'       <a href="#" class="avatar">'
                                                 +'           <img  src="/static/'+data.sender_avatar+'" class="img-fluid rounded-circle">'
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
                    // $('#chat').scrollTop($('#chat')[0].scrollHeight);
                });
                $('#send_button').on('click', function () {
                    text = $('#input_mess').val();
                    console.log(text)
                        if (text != ''){
                            $('#input_mess').val('');
                            // conver_id = parseInt($('#send_button').attr('conversation_id'))
                       socket.emit('text', {msg: text});
                            date = new Date()
                        $('#chats').append(' <div class="chat chat-right">'
                                                  +'  <div class="chat-body">'
                                                  +'      <div class="chat-bubble">'
                                                  +'          <div class="chat-content">'
                                                  +'              <p>'+text+'</p>'
                                                  +'              <span class="chat-time">'
                                                  +date.getHours()+
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

