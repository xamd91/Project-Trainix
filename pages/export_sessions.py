from flask import Response
from io import StringIO
import csv
from sqlalchemy.orm import aliased
from app import db
from models import Users, Departments, TrainingSessions, TrainingCourses, Attendance, Bookings


def export_sessions():

    Trainer = aliased(Users)

    sessions = (
        db.session.query(
            TrainingSessions,
            TrainingCourses.CourseName,
            Departments.DepartmentName,
            Trainer.FirstName,
            Trainer.LastName,
        )
        .join(
            TrainingCourses,
            TrainingSessions.CourseId == TrainingCourses.CourseId
        )
        .outerjoin(
            Departments,
            TrainingCourses.DepartmentId == Departments.DepartmentId
        )
        .join(
            Trainer,
            TrainingSessions.TrainerId == Trainer.UserId
        )
        .order_by(TrainingSessions.Date)
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Session ID",
        "Title",
        "Date",
        "Time",
        "Course",
        "Department",
        "Trainer",
        "Delivery Type",
        "Capacity",
        "Booked",
        "Seat Fill Rate",
        "Session Status",
        "Attendance Rate",
        "Approved Attendees"
    ])

    for session, course_name, department_name, trainer_first, trainer_last in sessions:

        bookings = (
            db.session.query(
                Users.FirstName,
                Users.LastName,
                Attendance.AttendanceStatus
            )
            .join(Bookings, Users.UserId == Bookings.UserId)
            .outerjoin(
                Attendance,
                Attendance.BookingId == Bookings.BookingId
            )
            .filter(
                Bookings.SessionId == session.SessionId,
                Bookings.Status == "Approved"
            )
            .all()
        )

        attendee_list = []

        attended = 0
        absent = 0

        for first, last, attendance in bookings:

            attendee_list.append(
                f"{first} {last}"
                + (
                    f" ({attendance})"
                    if attendance else ""
                )
            )

            if attendance == "Attended":
                attended += 1
            elif attendance == "Absent":
                absent += 1

        if session.Capacity:
            fill_rate = round((session.Booked / session.Capacity) * 100, 1)
        else:
            fill_rate = 0

        if session.Status == "Completed" and (attended + absent):

            attendance_rate = round(
                attended / (attended + absent) * 100,
                1
            )

            attendance_rate = f"{attendance_rate}%"

        else:
            attendance_rate = "N/A"

        writer.writerow([
            session.SessionId,
            session.Title,
            session.Date,
            session.Time.strftime('%I:%M %p'),
            course_name,
            department_name,
            f"{trainer_first} {trainer_last}",
            session.DeliveryType,
            session.Capacity,
            session.Booked,
            f"{fill_rate}%",
            session.Status,
            attendance_rate,
            ", ".join(attendee_list)
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=sessions_export.csv"
        }
    )