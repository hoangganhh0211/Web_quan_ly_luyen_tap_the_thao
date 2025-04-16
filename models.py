from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Bảng người dùng
class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # 'user' hoặc 'admin'
    height = db.Column(db.Float)
    weight = db.Column(db.Float)

    workouts = db.relationship("WorkoutHistory", backref="user", lazy=True)
    nutrition_plans = db.relationship("NutritionPlan", backref="user", lazy=True)

# Bảng bài tập
class Workout(db.Model):
    __tablename__ = "workouts"
    workout_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255))

    workout_history = db.relationship("WorkoutHistory", backref="workout", lazy=True)

# Bảng lịch sử tập luyện
class WorkoutHistory(db.Model):
    __tablename__ = "workout_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.workout_id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration_minutes = db.Column(db.Integer)

# Bảng kế hoạch dinh dưỡng
class NutritionPlan(db.Model):
    __tablename__ = "nutrition_plans"
    nutrition_plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    calories_per_day = db.Column(db.Float)