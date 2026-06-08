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
    DepartmentId = db.Column(db.Integer, db.ForeignKey('departments.DepartmentId'), nullable=True)
    ManagerId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=True)
    Role = db.Column(Enum("Learner", "Manager", "Trainer", "Admin", name="user_role"), nullable=True)
    department = db.relationship('Departments', foreign_keys=[DepartmentId], back_populates='users')
    manager = db.relationship('Users', remote_side=[UserId], backref='subordinates')
    bookings = db.relationship('Bookings', back_populates='user')
    attendance_records = db.relationship('Attendance', back_populates='user')
    training_sessions = db.relationship('TrainingSessions', foreign_keys='TrainingSessions.TrainerId', back_populates='trainer')

class TrainingSessions(db.Model):
    __tablename__ = "training_sessions"
    SessionId = db.Column(db.Integer, primary_key=True, nullable=False)
    CourseId = db.Column(db.Integer, db.ForeignKey('training_courses.CourseId'), nullable=False)
    TrainerId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=False)
    Title = db.Column(db.String(200), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    Time = db.Column(db.Time, nullable=False)
    Location = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    Prerequisites = db.Column(db.Text, nullable=True)
    Capacity = db.Column(db.Integer, nullable=False)
    DeliveryType = db.Column(Enum("Face-to-Face", "Online", name="delivery_type"), nullable=False)
    Booked = db.Column(db.Integer, nullable=True, default=0)
    trainer = db.relationship("Users", foreign_keys=[TrainerId], back_populates='training_sessions')
    course = db.relationship('TrainingCourses', back_populates='sessions')
    bookings = db.relationship('Bookings', back_populates='session')
    
class TrainingCourses(db.Model):
    __tablename__ = "training_courses"
    CourseId = db.Column(db.Integer, primary_key=True, nullable=False)
    CourseName = db.Column(db.String(200), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    DepartmentId = db.Column(db.Integer, db.ForeignKey('departments.DepartmentId'), nullable=True)
    sessions = db.relationship('TrainingSessions', back_populates='course')
    department = db.relationship('Departments', back_populates='courses')

class Bookings(db.Model):
    __tablename__ = "bookings"
    BookingId = db.Column(db.Integer, primary_key=True, nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=False)
    SessionId = db.Column(db.Integer, db.ForeignKey('training_sessions.SessionId'), nullable=False)
    BookingDate = db.Column(db.DateTime, nullable=False)
    Status = db.Column(Enum("Pending Approval", "Approved", "Rejected", "Cancelled", name="status"), nullable=False)
    ManagerApproval = db.Column(Enum("Yes", "No", name="manager_approval"), nullable=False)
    Notes = db.Column(db.Text, nullable=True)
    session = db.relationship('TrainingSessions', foreign_keys=[SessionId], back_populates='bookings')
    user = db.relationship('Users', foreign_keys=[UserId], back_populates='bookings')
    attendance = db.relationship('Attendance', back_populates='booking', uselist=False)

class Attendance(db.Model):
    __tablename__ = "attendance"
    AttendanceId = db.Column(db.Integer, primary_key=True, nullable=False)
    BookingId = db.Column(db.Integer, db.ForeignKey('bookings.BookingId'), nullable=False)
    UserId = db.Column(db.Integer,db.ForeignKey('users.UserId'), nullable=True )
    AttendanceStatus = db.Column(Enum("Attended", "Absent", "N/A", name="attendance_mark"), nullable=False, default="N/A")
    Comments = db.Column(db.Text, nullable=True)
    user = db.relationship('Users', foreign_keys=[UserId], back_populates='attendance_records')
    booking = db.relationship('Bookings', back_populates='attendance')

class Departments(db.Model):
    __tablename__ = "departments"
    DepartmentId = db.Column(db.Integer, primary_key=True, nullable=False)
    DepartmentName = db.Column(db.String(100), nullable=False)
    ManagerId = db.Column(db.Integer, db.ForeignKey('users.UserId'), nullable=True)
    users = db.relationship('Users', foreign_keys='Users.DepartmentId', back_populates='department')
    manager = db.relationship('Users', foreign_keys=[ManagerId])
    courses = db.relationship('TrainingCourses', back_populates='department')