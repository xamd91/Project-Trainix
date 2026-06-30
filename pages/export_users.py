from flask import Response
from io import StringIO
import csv

from app import db
from models import (
    Users,
    Departments,
    Bookings,
    TrainingSessions,
    TrainingCourses,
    Attendance,
)


def export_users():

    learners = (
        db.session.query(
            Users,
            Departments.DepartmentName
        )
        .outerjoin(
            Departments,
            Users.DepartmentId == Departments.DepartmentId
        )
        .filter(Users.Role == "Learner")
        .order_by(Users.LastName, Users.FirstName)
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Learner ID",
        "First Name",
        "Last Name",
        "Email",
        "Department",

        "Total Bookings",
        "Pending Approvals",
        "Approved",
        "Cancelled",
        "Rejected",

        "Attended",
        "Absent",
        "Attendance Rate",

        "Upcoming Confirmed Sessions",
        "Completed Session History"
    ])

    for learner, department in learners:

        bookings = (
            db.session.query(
                Bookings,
                TrainingSessions,
                TrainingCourses.CourseName,
                Attendance.AttendanceStatus
            )
            .join(
                TrainingSessions,
                Bookings.SessionId == TrainingSessions.SessionId
            )
            .join(
                TrainingCourses,
                TrainingSessions.CourseId == TrainingCourses.CourseId
            )
            .outerjoin(
                Attendance,
                Attendance.BookingId == Bookings.BookingId
            )
            .filter(Bookings.UserId == learner.UserId)
            .order_by(TrainingSessions.Date)
            .all()
        )

        total_bookings = len(bookings)

        pending = 0
        approved = 0
        cancelled = 0
        rejected = 0

        attended = 0
        absent = 0

        upcoming_sessions = []
        completed_sessions = []

        for booking, session, course_name, attendance in bookings:

            # Booking status counts
            if booking.Status == "Pending Approval":
                pending += 1

            elif booking.Status == "Approved":
                approved += 1

            elif booking.Status == "Cancelled":
                cancelled += 1

            elif booking.Status == "Rejected":
                rejected += 1

            # Upcoming confirmed sessions
            if (
                booking.Status == "Approved"
                and session.Status != "Completed"
            ):
                upcoming_sessions.append(
                    f"{course_name} ({session.Date})"
                )

            # Completed session history
            if session.Status == "Completed":

                status = attendance if attendance else "N/A"

                completed_sessions.append(
                    f"{course_name} ({status})"
                )

                if attendance == "Attended":
                    attended += 1

                elif attendance == "Absent":
                    absent += 1

        if attended + absent:
            attendance_rate = round(
                attended / (attended + absent) * 100,
                1
            )
            attendance_rate = f"{attendance_rate}%"
        else:
            attendance_rate = "N/A"

        writer.writerow([
            learner.UserId,
            learner.FirstName,
            learner.LastName,
            learner.Email,
            department,

            total_bookings,
            pending,
            approved,
            cancelled,
            rejected,

            attended,
            absent,
            attendance_rate,

            ", ".join(upcoming_sessions),
            ", ".join(completed_sessions)
        ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
                "attachment; filename=users_export.csv"
        }
    )