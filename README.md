#  Web Quản Lý Luyện Tập Thể Thao

Ứng dụng web giúp người dùng theo dõi quá trình luyện tập thể thao, quản lý bài tập và xây dựng kế hoạch dinh dưỡng một cách thông minh và tiện lợi.

---

##  Tính năng chính

###  Quản lý người dùng
- Đăng ký, đăng nhập, cập nhật hồ sơ cá nhân.
- Quản lý thông tin cá nhân: chiều cao, cân nặng.
- Xem lại lịch sử luyện tập cá nhân.

###  Quản lý bài tập
- Xem danh sách các bài tập có video hướng dẫn cụ thể.
- Tạo bài tập cá nhân phù hợp với từng người dùng.
- Theo dõi tiến độ tập luyện qua lịch sử và thời gian luyện tập.

###  Quản lý chế độ ăn uống
- Tạo kế hoạch dinh dưỡng phù hợp với mục tiêu tăng/giảm cân.
- Tính tổng calo mỗi ngày từ thực đơn đã nhập.
- Gợi ý thực đơn mẫu cho từng mục tiêu.

---

## Công nghệ sử dụng

- **Flask** – Python web framework
- **Flask-SQLAlchemy** – ORM để quản lý cơ sở dữ liệu
- **SQLite** – Cơ sở dữ liệu mặc định, có thể mở rộng sang PostgreSQL / MySQL
- **HTML/CSS/JS** – Giao diện người dùng (tuỳ biến thêm)

---

##  Mô hình cơ sở dữ liệu

### Bảng `users`
- `user_id`, `username`, `email`, `password`, `role`, `height`, `weight`

### Bảng `workouts`
- `workout_id`, `title`, `description`, `video_url`

### Bảng `workout_history`
- `id`, `user_id`, `workout_id`, `date`, `duration_minutes`

### Bảng `nutrition_plans`
- `nutrition_plan_id`, `user_id`, `plan_name`, `calories_per_day`

---


