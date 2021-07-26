$(document).ready(function (e) {
    $('#get_log_month').on('click', function () {
        var time = $('#log_month').val()
        if (time != ''){
        month = (time.split("-")[1])
        year = (time.split("-")[0])
        console.log('aaaaaaaa')
         window.location.assign('http://localhost:5000/admin/get_logs?month='+month+'&year='+year)
         }
    });


        $('#search_image').on('click', function () {
    var time = $('#time_image').val()
    console.log(time)
    if (time != ''){
        day = parseInt(time.split("/")[0]).toString()
        month = parseInt(time.split("/")[1]).toString()
        year = parseInt(time.split("/")[2]).toString()
        window.location.assign('http://localhost:5000/admin/get_stranger?m='+month+'&y='+year+'&d='+day)
    }

    });
});



function render_search(data){
    var time_in = data.time_in
                    if (data.time_in == null){
                        time_in = 'NULL'
                    }

                    var time_out = data.time_out
                    if (data.time_out == null){
                        time_out = 'NULL'
                    }

                    var css_tag_in = ''
                    if (data.tag_in == 1)
                        css_tag_in = 'fa fa-check text-success'
                    else if (data.tag_in == 2)
                        css_tag_in = 'fa fa-check text-danger'
                    else
                        css_tag_in = 'fa fa-circle-thin'

                    var css_tag_out = ''
                    if (data.tag_out== 1)
                        css_tag_out = 'fa fa-check text-success'
                    else if (data.tag_out == 2)
                        css_tag_out = 'fa fa-check text-danger'
                    else
                        css_tag_out = 'fa fa-circle-thin'

                    $('#show_log_emp').html('')
                    $('#show_log_emp').append('<tr>'
                                        +'<td id = "user_id_log">'+data.user_id+'</td>'
                                        +'<td id = "date_log">'+data.date+'</td>'
                                        +'<td id="time_in">'+time_in+'</td>'
                                        +'<td id="time_out">'+time_out+'</td>'
                                        +'<td><span class="first-off"><i class="'+css_tag_in+'"></i></span> </td>'
                                        +'<td><span class="first-off"><i class="'+css_tag_out+'"></i></span> </td>'

                                        +'<td class="text-right">'
                                        +'    <div class="dropdown dropdown-action">'
                                        +'        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>'
                                        +'        <div class="dropdown-menu dropdown-menu-right">'
                                        +'            <a class="dropdown-item" href="#" onclick="showModal()"><i class="fa fa-pencil m-r-5" ></i> Chỉnh sửa</a>'
                                        +'        </div>'
                                        +'    </div>'
                                        +'</td>'
                                    +'</tr>')

                }



$(document).ready(function (e) {
    $('#log_emp_search').on('click', function () {

        var time = $('#time_search').val().trim()
        var user_id = $('#emp_id_search').val()
        if (time != '' && user_id != ''){
        var form_data = new FormData();
        form_data.append('user_id', user_id)
        form_data.append('time', time)
        console.log(time)
        console.log(user_id)



        $.ajax({
            url: '/admin/get_log_post', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                if (response.status != 200){
                    alert(response.message)
                }
                else{
//                    data = response.data
                    render_search(response.data)
                }

            },
            error: function (response) {
                console.log(response.status)
                alert(response.message)
            }
        });
        }
    });
});
//
//
function showModal(){
       var user_id = parseInt($('#user_id_log').text())
       var date = $('#date_log').text()
       var time_in = $('#time_in').text()
       var time_out = $('#time_out').text()

       if (time_in != 'NULL' && time_out != 'NULL')
           alert("Log đã đủ, không được sửa")
       else{
           $('#time_update').html("")
           if (time_in == 'NULL'){
               $('#time_update').append('<div class="form-group form-focus">'
                           +'<label class="focus-label">Time CheckIn</label>'
                           +'<input type="time" class="form-control floating" id="u_time_in">'
                       +'</div>')
           }

           if (time_out == 'NULL'){
               $('#time_update').append('<div class="form-group form-focus">'
                           +'<label class="focus-label">Time CheckOut</label>'
                           +'<input type="time" class="form-control floating" id="u_time_out">'
                       +'</div>')
           }
           $('#update_log_modal').modal('show')
       }
}


$(document).ready(function (e) {
    $('#button_update_log').on('click', function () {
        var time_in = $('#u_time_in').val()
        var time_out = $('#u_time_out').val()
        var check = 1
        if (time_out == '' && time_in == '')
            check = 0
        if (time_in === undefined && time_out == '')
            check = 0
        if (time_out === undefined && time_in == '')
            check = 0

        if (check == 1){
            var user_id = parseInt($('#user_id_log').text())
            var date = $('#date_log').text()
            var form_data = new FormData()
            form_data.append('user_id', user_id)
            form_data.append('date', date)
            form_data.append('time_in', time_in)
            form_data.append('time_out', time_out)


            $.ajax({
            url: '/admin/update_log', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'PUT',
            success: function (response) {
                alert(response.message)
                if(response.status == 200){
                    $('#update_log_modal').modal('hide')
                    render_search(response.data)
                }
//
            },
            error: function (response) {
                console.log(response.status)
                alert(response.message)
            }
        });
        }
    });
});