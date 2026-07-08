from notifications.user_notifications import attendance_marked
from flask import session, redirect, url_for, request, jsonify
from app import db
from datetime import datetime, date
from models import Users, Bookings, TrainingSessions

def mark_attendance():

    if request.method == "POST":

        session_id = request.form.get('session_id')

        training_session = TrainingSessions.query.filter_by(SessionId=session_id).first()

        bookings = (
            Bookings.query
            .join(Bookings.session)
            .filter(
                TrainingSessions.SessionId == session_id,
                Bookings.Status == 'Approved',
                Bookings.CompletedAt.is_(None)
            )
            .all()
        )

        # Bookings.query.filter_by(SessionId=session_id).all()

        booking_lookup = {
            booking.UserId: booking
            for booking in bookings
        }

        for user_id, booking in booking_lookup.items():

            valid_statuses = ["Attended", "Absent"]

            status = request.form.get(str(user_id))
            comment = request.form.get(f"comment-{user_id}")

            # print(
            #     f"Session: {session_id}, "
            #     f"User: {user_id}, "
            #     f"Attendance: {status}"
            # )

            if not status:
                return jsonify({
                    "status": "error",
                    "message": "Please mark attendance for all attendees before submitting."
                }), 400
            
            status = status.capitalize()

            if status not in valid_statuses:
                return jsonify({
                    "status": "error",
                    "message": "Please mark attendance for all attendees before submitting."
                }), 400
            
            print(booking.attendance)
            
            old_status = booking.attendance.AttendanceStatus

            was_marked = old_status in valid_statuses

            booking.attendance.AttendanceStatus = status

            if status == "Attended":
                booking.CompletedAt = date.today()

            if not was_marked:
                booking.session.Marked += 1

            if comment is not None:
                booking.attendance.Comments = comment

            if old_status != status:
                attendance_marked(
                    user=booking.user,
                    session=booking.session,
                    status=status,
                )

        db.session.commit()


        return jsonify({
            "status": "success",
            "message": "Attendance records saved successfully!",
        }), 201

        return redirect(url_for("attendance_management"))