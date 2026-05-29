from sqlalchemy.orm import backref
from app import db 
from sqlalchemy import Enum

class Users(db.Model):
    __tablename__ = "users"
    UserId = db.Column(db.Integer, primary_key=True, nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(11), nullable=False, unique=True)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    JobTitle = db.Column(db.String(100), nullable=True)
    BusinessArea = db.Column(db.String(100), nullable=True)
    Role = db.Column(Enum("Learner", "Manager", "Trainer", "Admin", name="user_roles"), nullable=True)
    ManagerId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=True)

class TrainingSessions(db.Model):
    __tablename__ = "training_sessions"
    SessionId = db.Column(db.Integer, primary_key=True, nullable=False)
    CourseId = db.Column(db.Integer, db.ForeignKey('training_courses.courseId'), nullable=False)
    TrainerId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=False)
    Title = db.Column(db.String(200), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    Time = db.Column(db.Time, nullable=False)
    Location = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Capacity = db.Column(db.Integer, nullable=False)
    DeliveryType = db.Column(Enum("Face-to-Face", "Online", name="delivery_type"), nullable=False)

class TrainingCourses(db.Model):
    __tablename__ = "training_courses"
    CourseId = db.Column(db.Integer, primary_key=True, nullable=False)
    CourseName = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    BusinessArea = db.Column(db.String(100), nullable=False)

class Bookings(db.Model):
    __tablename__ = "bookings"
    BookingId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=False)
    SessionId = db.Column(db.Integer, db.ForeignKey('training_sessions.sessionId'), nullable=False)
    BookingDate = db.Column(db.DateTime, nullable=False)
    Status = db.Column(Enum("Pending Approval", "Approved", "Rejected", "Cancelled", name="status"), nullable=False)
    ManagerApproval = db.Column(Enum("Yes", "No", name="manager_approval"), nullable=False)
    Notes = db.Column(db.Text, nullable=True)

class Attendance(db.Model):
    __tablename__ = "attendance"
    AttendanceId = db.Column(db.Integer, primary_key=True, nullable=False)
    BookingId = db.Column(db.Integer, db.ForeignKey('bookings.bookingId'), nullable=False)
    AttendanceStatus = db.Column(Enum("Attended", "Absent", name="attendance_status"), nullable=False)
    Comments = db.Column(db.Text, nullable=True)