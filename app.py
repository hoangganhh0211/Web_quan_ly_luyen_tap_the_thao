from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from models import *
from datetime import date

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@Localhost:5432/Web_quan_ly_luyen_tap_the_thao'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Trang chủ
@app.route("/",)
def index():
    return render_template("index.html", name = session.get("username"))

# Chức năng đăng ký
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        height = request.form.get("height")
        weight = request.form.get("weight")

        # Kiểm tra xem người dùng đã tồn tại chưa
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="Tên đăng nhập đã tồn tại")

        # Tạo người dùng mới
        new_user = User(username=username, email=email, password=password, height=height, weight=weight)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))   
    return render_template("register.html")


# Chức năng đăng nhập
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Truy vấn người dùng trong bảng users
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
            return render_template("index.html", error="Sai tên đăng nhập hoặc mật khẩu")

    return render_template("index.html")

# Chức năng đăng xuất
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Chức năng xem thông tin cá nhân
@app.route("/show_profile")
def show_profile():
    if "username" in session:
        username = session["username"]
        users = User.query.filter_by(username=username).first()
    return render_template("showprofile.html", users=users)

# Chức năng cập nhật thông tin cá nhân
@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():
    if "username" in session:
        username = session["username"]
        users = User.query.filter_by(username=username).first()

        if request.method == "POST":
            users.height = request.form.get("height")
            users.weight = request.form.get("weight")
            db.session.commit()
            return redirect(url_for("show_profile"))

        return render_template("update_profile.html", users=users)

# Chức năng thêm bài tập
@app.route("/add_workout", methods=["GET", "POST"])
def add_workout():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        video_url = request.form.get("video_url")

        # Tạo bài tập mới
        new_workout = Workout(title=title, description=description, video_url=video_url)
        db.session.add(new_workout)
        db.session.commit()
        return redirect(url_for("show_workout"))
    return render_template("add_workout.html")

# Chức năng xem danh sách bài tập
@app.route("/show_workout")
def show_workout():
    workouts = Workout.query.all()
    return render_template("show_workout.html", workouts=workouts)

# Chức năng xem chi tiết bài tập và lưu vào lịch sử tập luyện
@app.route("/workout_info/<int:id>")
def workout_info(id):
    workout = Workout.query.get_or_404(id)
    return render_template("workout_info.html", workout=workout)

# Chức năng chỉnh sửa bài tập
@app.route("/update_workout/<int:id>", methods=["GET", "POST"])
def update_workout(id):
    workout = Workout.query.get_or_404(id)
    if request.method == "POST":
        workout.title = request.form.get("title")
        workout.description = request.form.get("description")
        workout.video_url = request.form.get("video_url")
        db.session.commit()
        return redirect(url_for("show_workout"))
    return render_template("update_workout.html", workout=workout)

# Chức năng xóa bài tập
@app.route("/delete_workout/<int:id>")
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return redirect(url_for("show_workout"))

# Chức năng xem kế hoạch dinh dưỡng
@app.route("/show_nutrition_plan")
def show_nutrition_plan():
    nutrition_plans = NutritionPlan.query.all()
    return render_template("show_nutrition_plan.html", nutrition_plans=nutrition_plans)

# Chức năng thêm kế hoạch dinh dưỡng
@app.route("/add_nutrition_plan", methods=["GET", "POST"])
def add_nutrition_plan():
    if request.method == "POST":
        plan_name = request.form.get("plan_name")
        plan_description = request.form.get("plan_description")
        food_item = request.form.get("food_item")
        calories = request.form.get("calories")

        # Tạo kế hoạch dinh dưỡng mới
        new_plan = NutritionPlan(plan_name=plan_name, plan_description=plan_description, food_item=food_item, calories=calories)
        db.session.add(new_plan)
        db.session.commit()
        return redirect(url_for("show_nutrition_plan"))
    return render_template("add_nutrition_plan.html")

# Chức năng xem chi tiết kế hoạch dinh dưỡng
@app.route("/nutrition_plan_detail/<int:id>")
def nutrition_plan_detail(id):
    nutrition_plan = NutritionPlan.query.get_or_404(id)
    return render_template("nutrition_plan_detail.html", nutrition_plan=nutrition_plan)

# Chức năng chỉnh sửa kế hoạch dinh dưỡng
@app.route("/update_nutrition_plan/<int:id>", methods=["GET", "POST"])
def update_nutrition_plan(id):
    nutrition_plan = NutritionPlan.query.get_or_404(id)
    if request.method == "POST":
        nutrition_plan.plan_name = request.form.get("plan_name")
        nutrition_plan.plan_description = request.form.get("plan_description")
        nutrition_plan.food_item = request.form.get("food_item")
        nutrition_plan.calories = request.form.get("calories")
        db.session.commit()
        return redirect(url_for("show_nutrition_plan"))
    return render_template("update_nutrition_plan.html", nutrition_plan=nutrition_plan)

# Chức năng xóa kế hoạch dinh dưỡng
@app.route("/delete_nutrition_plan/<int:id>")
def delete_nutrition_plan(id):
    nutrition_plan = NutritionPlan.query.get_or_404(id)
    db.session.delete(nutrition_plan)
    db.session.commit()
    return redirect(url_for("show_nutrition_plan"))

# Chức năng xem lịch sử tập luyện
@app.route("/show_workout_history")
def show_workout_history():
    username = session.get("username")
    user = User.query.filter_by(username=username).first()

    if not user:
        return "User không tồn tại", 404

    workout_histories = WorkoutHistory.query.filter_by(user_id=user.user_id).all()
    return render_template("show_workout_history.html", workout_histories=workout_histories)


# Chức năng thêm lịch sử tập luyện
@app.route("/add_workout_history/<int:id>", methods=["GET","POST"])
def add_workout_history(id):
    username = session.get("username")
    user = User.query.filter_by(username=username).first()  # Lấy user từ username
    if not user:
        return "User không tồn tại", 404

    workout = Workout.query.get_or_404(id)
    date_today = date.today()

    # Kiểm tra lịch sử đã tồn tại
    existing_history = WorkoutHistory.query.filter_by(user_id=user.user_id, workout_id=id, date=date_today).first()

    if existing_history:
        return redirect(url_for("show_workout_history"))

    # Tạo lịch sử mới
    new_history = WorkoutHistory(user_id=user.user_id, workout_id=id, date=date_today)
    db.session.add(new_history)
    db.session.commit()
    return redirect(url_for("show_workout_history"))
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)