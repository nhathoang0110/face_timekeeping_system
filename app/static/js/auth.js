$(document).ready(function (e) {
    $('#register').on('click', function () {
        var form_data = new FormData();

        var name = $('#fullname').val()
        var mail = $('#mail').val()
        var date_of_birth = $('#date_of_birth').val()
        var phone = $('#phone').val()
        var salary = $('#salary').val()
        var file1 = document.getElementById('file1').files[0]
        var file2 = document.getElementById('file2').files[0]
        var file3 = document.getElementById('file3').files[0]

        if (validateEmail(mail) == false){
            alert("Email không đúng định dạng")
        }else if(validatePhone(phone) == false){
            alert("Số điện thoại không đúng định dạng")
        }
        else if(moment(date_of_birth, "DD/MM/YYYY").toDate().getTime() >= new Date().getTime()){
            alert("Ngày sinh không được lớn hơn ngày hiện tại")
        }
        else{


        if (name != '' && mail != '' &&date_of_birth != '' &&phone != '' &&salary != '' &&file1 != undefined &&file2 != undefined && file3 != undefined){
             console.log(file1)
        form_data.append('name', name)
         form_data.append('mail', mail)
         form_data.append('date_of_birth', date_of_birth)
         form_data.append('phone', phone)
         form_data.append('salary', salary)
         form_data.append('file1', file1)
         form_data.append('file2', file2)
         form_data.append('file3', file3)

        $('#modalLoading').modal('show');


        $.ajax({
            url: '/admin/register', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
            success: function (response) {
                $('#modalLoading').modal('hide');
                console.log(response.status);
                alert(response.message);
            },
            error: function (response) {
                $('#modalLoading').modal('hide');
                console.log('fail');
                alert(response.message);
            }
        });
//         $('#modalLoading').modal('hide');
        }
        else{
            alert("Hãy nhập đủ thông tin")
        }
        }

    });
});

function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function validatePhone(phone) {
  var re = /^\d+$/;
  return re.test(phone);
}