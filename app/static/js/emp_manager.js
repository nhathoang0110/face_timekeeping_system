$(document).ready(function (e) {
    $('#update').on('click', function () {

        var form_data = new FormData();

        var id = parseInt($('#user_id').attr('user_id'))
        var name = $('#name').val().trim()
        var date_of_birth = $('#date_of_birth').val()
        var phone = $('#phone').val().trim()

        if(name == '' || date_of_birth =='' || phone == ''){
            alert("Hãy nhập đầy đủ thông tin")
        }
        else if(validatePhone(phone) == false){
            alert("Số điện thoại không đúng định dạng")
        }
        else if(moment(date_of_birth, "DD/MM/YYYY").toDate().getTime() >= new Date().getTime()){
            alert("Ngày sinh không được lớn hơn ngày hiện tại")
        }
        else{

        form_data.append('name', name)
         form_data.append('date_of_birth', date_of_birth)
         form_data.append('phone', phone)
         form_data.append('id', id)

        console.log(id)



        $.ajax({
            url: '/admin/update_emp', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'PUT',
            success: function (response) {
                console.log(response.status)
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


$(document).ready(function (e) {
    $('#search_emp').on('click', function () {

        var name = $('#name_emp_search').val().trim()
        if (name != ''){
        var form_data = new FormData();
        form_data.append('name', name)



        $.ajax({
            url: '/admin/search', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                console.log(response.data)
                data = response.data
                if (data.length > 0){
                    $('#list_emp').html("")
                    for (i = 0 ; i < data.length; i++){
                    $('#list_emp').append('<tr>'
                    +'<td>'
                    +'    <img width="28" height="28" src="/static/'+ data[i].avatar+'" class="rounded-circle" alt=""> <h2>'+data[i].name+'</h2>'
                    +'</td>'
                    +'<td>'+data[i].id+'</td>'
                    +'<td>'+data[i].mail+'</td>'
                    +'<td>'+data[i].phone+'</td>'
                    +'<td>'+data[i].date_of_birth+'</td>'
                    +'<td class="text-right">'
                    +'    <div class="dropdown dropdown-action">'
                    +'        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>'
                    +'        <div class="dropdown-menu dropdown-menu-right">'
                    +'            <a class="dropdown-item" href="/admin/update_emp?id='+data[i].id+'"><i class="fa fa-pencil m-r-5"></i> Chỉnh sửa</a>'
                    +'            <a class="dropdown-item" href="#" data-toggle="modal" data-target="#delete_employee"><i class="fa fa-trash-o m-r-5"></i> Xóa</a>'
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




$(document).ready(function (e) {
    $('#button_del').on('click', function () {
        var id =  parseInt($('#delete_employee').attr('user_id_del'))
        var form_data = new FormData();
        form_data.append('user_id', id)
        console.log(id)




        $.ajax({
            url: '/admin/delete_emp', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'DELETE',
            success: function (response) {
                hideModal()
                data = response.data
                console.log(data)
                if (response.status == 200){
                    $('#list_emp').html("")
                if (data.length > 0){

                    for (i = 0 ; i < data.length; i++){
                    $('#list_emp').append('<tr>'
                    +'<td>'
                    +'    <img width="28" height="28" src="/static/'+ data[i].avatar+'" class="rounded-circle" alt=""> <h2>'+data[i].name+'</h2>'
                    +'</td>'
                    +'<td>'+data[i].id+'</td>'
                    +'<td>'+data[i].mail+'</td>'
                    +'<td>'+data[i].phone+'</td>'
                    +'<td>'+data[i].date_of_birth+'</td>'
                    +'<td class="text-right">'
                    +'    <div class="dropdown dropdown-action">'
                    +'        <a href="#" class="action-icon dropdown-toggle" data-toggle="dropdown" aria-expanded="false"><i class="fa fa-ellipsis-v"></i></a>'
                    +'        <div class="dropdown-menu dropdown-menu-right">'
                    +'            <a class="dropdown-item" href="/admin/update_emp?id='+data[i].id+'"><i class="fa fa-pencil m-r-5"></i> Chỉnh sửa</a>'
                    +'            <a class="dropdown-item" href="#" onclick="showModal('+data[i].id+')" ><i class="fa fa-trash-o m-r-5"></i> Xóa</a>'
                    +'        </div>'
                    +'    </div>'
                    +'</td>'
                    +'</tr>')
                    }
                }
                }



                alert(response.message)
                   
            },
            error: function (response) {
                
                    alert(response.message)
            }
        });


    });
});


function showModal(id){
    $('#delete_employee').attr('user_id_del' , id)
    $('#delete_employee').modal('show');
}
function hideModal(){
    $('#delete_employee').attr('user_id_del' , "")
    $('#delete_employee').modal('hide');
}

function showModalImg(id){
//    $('#delete_employee').attr('user_id_del' , id)
    form_data = new FormData()
    form_data.append('user_id', id)
 $.ajax({
            url: '/admin/get_images', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                paths = response.paths
                $('#image_user_1').attr('src', paths[0])
                $('#image_user_2').attr('src', paths[1])
                $('#image_user_3').attr('src', paths[2])
                $('#image_employee').modal('show');

            },
            error: function (response) {
                console.log(response.status)
                alert(response.message)
            }
        });
//
//console.log('/static/img/blog/' + id + '_1.jpg')
//    $('#image_user_1').attr('src', '/static/img/blog/' + id + '_1.jpg')
//    $('#image_user_2').attr('src', '/static/img/blog/' + id + '_2.jpg')
//    $('#image_user_3').attr('src', '/static/img/blog/' + id + '_3.jpg')
//    $('#image_employee').modal('show');
}
function hideModal(){
    $('#delete_employee').attr('user_id_del' , "")
    $('#delete_employee').modal('hide');
}

function validatePhone(phone) {
  var re = /^\d+$/;
  return re.test(phone);
}