from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Attendance, Departments, Notifications
from app import db
from sqlalchemy import or_
from datetime import datetime
from zoneinfo import ZoneInfo
from urllib.parse import quote

def outlook_calendar_link(session_obj):
        start = datetime.combine(session_obj.Date, session_obj.Time)
        end = datetime.combine(session_obj.Date, session_obj.EndTime)

        params = {
            "path": "/calendar/action/compose",
            "rru": "addevent",
            "subject": session_obj.Title,
            "startdt": start.isoformat(),
            "enddt": end.isoformat(),
            "body": session_obj.Description or "",
            "location": session_obj.Location or "",
        }

        base = "https://outlook.office.com/calendar/0/deeplink/compose?"
        query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
        return base + query

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    tab = request.args.get('tab', 'bookings')

    user_id = session.get('user_id')
    user = Users.query.filter_by(UserId=user_id).first()
    
    attendance = Attendance.query.filter_by(UserId=session['user_id']).all()

    bookings = Bookings.query.filter_by(UserId=session['user_id']).all()

    manager = Users.query.filter_by(DepartmentId=user.DepartmentId, Role='Manager').first()

    upcoming_bookings = (
        Bookings.query
        .join(Bookings.session)
        .filter(
            or_(
                Bookings.Status == "Pending Approval",
                Bookings.Status == "Approved"
            ),
            Bookings.UserId == user_id,
            TrainingSessions.Status == "Not completed"
        )
        .order_by(TrainingSessions.Date.asc()).all()
    )

    upcoming_bookings = [
         b for b in upcoming_bookings
         if datetime.combine(b.session.Date, b.session.EndTime) > datetime.now()
    ]

    for booking in upcoming_bookings:
        booking.session.outlook_calendar_url = outlook_calendar_link(booking.session)

    inactive_bookings = (
        Bookings.query
        .join(Bookings.session)
        .filter(
            or_(
                Bookings.Status == "Rejected",
                Bookings.Status == "Cancelled",
                TrainingSessions.Status == "Cancelled"
            ),
            Bookings.UserId == user_id
        )
        .order_by(TrainingSessions.Date.desc()).all()
    )

    training_history = (
        Bookings.query
        .join(Bookings.session)
        .join(Bookings.attendance)
        .filter(
            Bookings.UserId == user_id,
            Bookings.Status == "Approved",
            TrainingSessions.Status == "Completed"
        )
        .order_by(TrainingSessions.Date.desc()).all()
    )
    
    departments = Departments.query.all()
    
    # notifications tab - IsRead is only used to drive the unread badge count per call.
    notifications = []
    if tab == "notifications":
        notifications = (
            Notifications.query
            .filter_by(UserId=user_id)
            .order_by(Notifications.CreatedAt.desc())
            .all()
        )

        UK_TZ = ZoneInfo("Europe/London")
        for notification in notifications:
            notification.CreatedAtLocal = notification.CreatedAt.replace(tzinfo=ZoneInfo("UTC")).astimezone(UK_TZ)

        unread_on_load = sum(1 for n in notifications if not n.IsRead)

        for notification in notifications:
            notification.IsRead = True
        db.session.commit()    

    return render_template(
        'account.html', 
        user=user, 
        tab=tab, 
        bookings=bookings, 
        upcoming_bookings=upcoming_bookings,
        inactive_bookings=inactive_bookings,
        training_history=training_history,
        attendance=attendance,
        departments=departments,
        notifications=notifications
        )