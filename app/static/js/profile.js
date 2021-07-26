$(document).ready(function (e) {
    $('#update').on('click', function () {
        var form_data = new FormData();

        var name = $('#name').val()
        var date_of_birth = $('#date_of_birth').val()
        var phone = $('#phone').val()


        form_data.append('name', name)
         form_data.append('date_of_birth', date_of_birth)
         form_data.append('phone', phone)
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



        $.ajax({
            url: '/update_profile', // point to server-side URL
            dataType: 'json', // what to expect back from server
            contentType: false,
            processData: false,
            data: form_data,
            type: 'POST',
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
    $('#update_pass').on('click', function () {
        var form_data = new FormData();

        var current_pass = $('#current_password').val()
        var new_pass = $('#new_password').val()
        var re_pass = $('#re_enter_new_password').val()

        if (current_pass == '' || new_pass == '' || re_pass == '')
            alert("Hãy nhập đủ các trường dữ liệu ")
        else if (new_pass != re_pass)
            alert("Mật khẩu mới không trùng khớp")
        else{
            form_data.append('current_password', current_pass)
            form_data.append('new_password', new_pass)
            form_data.append('re_enter_new_password', re_pass)
   
   
   
   
           $.ajax({
               url: '/update_password', // point to server-side URL
               dataType: 'json', // what to expect back from server
               contentType: false,
               processData: false,
               data: form_data,
               type: 'POST',
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

function validatePhone(phone) {
  var re = /^\d+$/;
  return re.test(phone);
}