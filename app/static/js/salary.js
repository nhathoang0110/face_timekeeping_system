$(document).ready(function (e) {
    $('#get_salaries').on('click', function () {
        var time = $('#salary_month').val()
        if (time != ''){
        month = (time.split("-")[1])
        year = (time.split("-")[0])

         window.location.assign('http://localhost:5000/admin/get_salaries?month='+month+'&year='+year)
        }

    });
});


$(document).ready(function (e) {
    $('#search_hard_salary').on('click', function () {

        var name = $('#emp_name_hard').val().trim()
        if (name != ''){
        var form_data = new FormData();
        form_data.append('name', name)




        $.ajax({
            url: '/admin/search_hard_salary', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                console.log(response.data)
                data = response.data
                if (data.length > 0){
                    $('#list_salary').html("")
                    for (i = 0 ; i < data.length; i++){
                    $('#list_salary').append('<tr>'
                                        +'<td>'
										+'	<img class="rounded-circle" src="/static/'+data[i].avatar+'" height="28" width="28" alt="">'+ data[i].name
                                        +'</td>'
                                        +'<td>'+data[i].id+'</td>'
                                        +'<td>'+data[i].mail+'</td>'
                                        +'<td>'+data[i].salary+' VND</td>'
                                        +'<td class="text-right">'
                                        +'    <div class="dropdown dropdown-action">'
                                        +'        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>'
                                        +'        <div class="dropdown-menu dropdown-menu-right">'
                                        +'            <a class="dropdown-item" href="#"  onclick="showModal('+data[i].id+')"><i class="fa fa-pencil m-r-5"></i> Sửa</a>'
                                        +'        </div>'
                                        +'    </div>'
                                        +'</td>'
                                    +'</tr>')
                    }
                }
                else
                    alert("Không tìm thấy nhân viên nào")

//                alert(response.message)
            },
            error: function (response) {
                console.log(response.status)
                alert(response.message)
            }
        });
        }
    });
});

function showModal(id){
    $('#update_salary').attr('user_id_update' , id)
    $('#update_salary').modal('show');
}
function hideModal(){
    $('#update_salary').attr('user_id_update' , "")
    $('#new_salary').val(0)
    $('#update_salary').modal('hide');
}


$(document).ready(function (e) {
    $('#button_update').on('click', function () {

        var id =  parseInt($('#update_salary').attr('user_id_update'))
        var new_salary = $('#new_salary').val()
        if (new_salary != 0){
        var form_data = new FormData();
        form_data.append('user_id', id)
        form_data.append('new_salary', new_salary)
        console.log(id)
        console.log(new_salary)




        $.ajax({
            url: '/admin/get_hard_salary', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                hideModal()
                data = response.data
                console.log(data)
                if (response.status == 200){
                    $('#list_salary').html("")
                    for (i = 0 ; i < data.length; i++){
                    $('#list_salary').append('<tr>'
                                        +'<td>'
										+'	<img class="rounded-circle" src="/static/'+data[i].avatar+'" height="28" width="28" alt="">' + data[i].name                                        +'</td>'
                                        +'<td>'+data[i].id+'</td>'
                                        +'<td>'+data[i].mail+'</td>'
                                        +'<td>'+data[i].salary+' VND</td>'
                                        +'<td class="text-right">'
                                        +'    <div class="dropdown dropdown-action">'
                                        +'        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>'
                                        +'        <div class="dropdown-menu dropdown-menu-right">'
                                        +'            <a class="dropdown-item" href="#" onclick="showModal('+data[i].id+')"><i class="fa fa-pencil m-r-5"></i> Sửa</a>'
                                        +'        </div>'
                                        +'    </div>'
                                        +'</td>'
                                    +'</tr>')
                    }
                }


                alert(response.message)
            },
            error: function (response) {
                console.log(response.status)
                alert(response.message)
            }
        });
        }

    });
});