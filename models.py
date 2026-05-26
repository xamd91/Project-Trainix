from sqlalchemy.orm import backref
from app import db 
from sqlalchemy import Enum

class Users(db.Model):
    __tablename__ = "users"
    userId = db.Column(db.Integer, primary_key=True, nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    jobTitle = db.Column(db.String(100), nullable=False)
    businessArea = db.Column(db.String(100), nullable=False)
    role = db.Column(Enum("learner", "manager", "trainer", "admin", name="user_roles"), nullable=False)
    managerId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=True)

class TrainingSessions(db.Model):
    __tablename__ = "training_sessions"
    sessionId = db.Column(db.Integer, primary_key=True, nullable=False)
    courseId = db.Column(db.Integer, db.ForeignKey('training_courses.courseId'), nullable=False)
    trainerId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    capacity = db.Column(db.Integer, nullable=False)
    deliveryType = db.Column(Enum("Face-to-Face", "Online", name="delivery_type"), nullable=False)

class TrainingCourses(db.Model):
    __tablename__ = "training_courses"
    courseId = db.Column(db.Integer, primary_key=True, nullable=False)
    courseName = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    businessArea = db.Column(db.String(100), nullable=False)

class Bookings(db.Model):
    __tablename__ = "bookings"
    bookingId = db.Column(db.Integer, primary_key=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    sessionId = db.Column(db.Integer, db.ForeignKey('training_sessions.sessionId'), nullable=False)
    bookingDate = db.Column(db.DateTime, nullable=False)
    status = db.Column(Enum("Pending Approval", "Approved", "Rejected", "Cancelled", name="status"), nullable=False)
    manager_approval = db.Column(Enum("Yes", "No", name="manager_approval"), nullable=False)
    notes = db.Column(db.Text, nullable=True)

class Attendance(db.Model):
    __tablename__ = "attendance"
    attendanceId = db.Column(db.Integer, primary_key=True, nullable=False)
    bookingId = db.Column(db.Integer, db.ForeignKey('bookings.bookingId'), nullable=False)
    attendanceStatus = db.Column(Enum("Attended", "Absent", name="attendance_status"), nullable=False)
    comments = db.Column(db.Text, nullable=True)