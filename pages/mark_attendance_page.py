from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime
from models import Users, Bookings, TrainingSessions

def mark_attendance():

    if request.method == "POST":

        session_id = request.form.get('session_id')

        print(session_id)

        bookings = Bookings.query.filter_by(SessionId=session_id).all()

        booking_lookup = {
            booking.UserId: booking
            for booking in bookings
        }

        for key, value in request.form.items():

            if key == "session_id":
                continue

            if not value:
                continue
            
            user_id = int(key)

            booking = booking_lookup.get(user_id)

            if not booking:
                continue

            booking.attendance.AttendanceStatus = value.capitalize()
            booking.session.Marked += 1


        db.session.commit()

        print(
            f"Session: {session_id}, "
            f"User: {user_id}, "
            f"Attendance: {value}"
        )

        return redirect(url_for("attendance_management"))