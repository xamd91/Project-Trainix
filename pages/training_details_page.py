from flask import render_template, session, redirect, url_for
from models import Users, TrainingSessions, TrainingCourses, Bookings
from app import db

def page(session_id):

    training_session = TrainingSessions.query.get(session_id)

    user_id = session.get('user_id')

    user = Users.query.filter_by(UserId=user_id).first()

    if training_session is None:
        return redirect(url_for('training_catalogue'))

    already_booked = (
        Bookings.query
        .filter(
            Bookings.SessionId==session_id, 
            Bookings.UserId==user_id,
            Bookings.Status != "Cancelled"
        )
        .first()
    )

    total_bookings = training_session.Booked
    remaining_slots = training_session.Capacity - total_bookings

    session_full = remaining_slots == 0

    return render_template("training_details.html", user=user, training_session=training_session, remaining_slots=remaining_slots, session_full=session_full, already_booked=already_booked)