# Hệ thống chấm công nhận diện khuôn mặt 

## Yêu cầu hệ thống

* Python >= 3.6
* OpenVINO toolkit 2021.2: Tải và cài đặt theo hướng dẫn ở https://docs.openvinotoolkit.org/2021.2/openvino_docs_install_guides_installing_openvino_linux.html, kiểm tra bằng việc chạy cell python lệnh "from openvino.inference_engine import IECore"
* MySQL 8.0 ( 8.0.23 or 8.0.25)

## Cài đặt

### Bước 1: Tải ứng dụng từ gitlab

`https://gitlab.com/is_soict/it4421_20202/1_chungdt/face_timekeeping_system.git`

### Bước 2: Cài đặt các thư viện cần thiết

`$ pip install -r requirements.txt`
### Bước 3: Tạo một database trống trong mysql

### Bước 4: Tạo file \instance\config.py với nội dung
`SECRET_KEY = 'p9Bv<3Eid9%$i2'`
`SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://database_username:database_password@database_ip/database_name'`


Ví dụ:
```
database_username: HOAMV
database_password: maivanhoa
database_ip: localhost
database_name: httt (database tạo ở bước 3)

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://HOAMV:maivanhoa@localhost/httt'
```

### Bước 5: Tạo các bảng  dữ liệu cho hệ thống

**Sử dụng Python REPL gõ lệnh sau**

`>>> from app import db, create_app`

`>>> db.create_all(app=create_app(1))`

### Bước 6: Tạo một user admin với mật khẩu là 1
Lưu ý: Các nhân viên được tạo mới bởi admin thì mật khẩu mặc định là 1
```
insert into users (name, mail, password, is_admin) values ('admin1', 'admin1@gmail.com', 'pbkdf2:sha256:150000$eeogIZfA$83270fa0f45da67aae54ebb4721cd4c6bf5e58218f876b760f9ff2eb41888ed3', 1);
```

## Chạy ứng dụng

Các bạn dùng terminal truy cập vào trong folder của dự án và gõ lệnh:

`$ python run.py`

Lúc này dự án đã được khởi chạy, hệ thống đã báo ứng dụng của chúng ta đang được chạy ở địa chỉ localhost và port là 5000. Lúc này các bạn chỉ cần lên trên trình duyệt truy cập vào địa chỉ sau:

`http://localhost:5000/login`
