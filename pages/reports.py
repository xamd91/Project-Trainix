from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses, Attendance
from sqlalchemy import func, or_
from app import db
from collections import defaultdict

def page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # if session['role'] != "admin":
    #      return redirect(url_for('login'))
    user_id = session.get('user_id') 

    admin = Users.query.filter_by(UserId=user_id).first()
    users = Users.query.all()
    tab = request.args.get('tab', 'overview')

    bookings = Bookings.query.all()

    normal_sessions = TrainingSessions.query.order_by(TrainingSessions.Date.asc()).all()
        
    total_booked = 0
    total_attended = 0

    for sess in normal_sessions:
        sess.attended_count = 0
        sess.booked_count = 0
        for booking in sess.bookings:
            if booking.Status in ['Approved', 'Completed']:
                total_booked += 1
                sess.booked_count += 1
                if booking.attendance and booking.attendance.AttendanceStatus == "Attended":
                    total_attended += 1
                    sess.attended_count += 1
        sess.attendance_rate = (
            round((sess.attended_count / sess.booked_count) * 100, 1)
            if sess.booked_count > 0
            else 0
        )
    
    if total_booked > 0:
        attendance_rate = round((total_attended / total_booked) * 100, 1)
    else:
        attendance_rate = 0

    total_booked_overview = 0
    total_attended_overview = 0

    completed_sessions = [s for s in normal_sessions if s.Status == "Completed"]

    for sess in completed_sessions:
        for booking in sess.bookings:
            if booking.Status in ['Approved', 'Completed']:
                total_booked_overview += 1

                if booking.attendance and booking.attendance.AttendanceStatus == "Attended":
                    total_attended_overview += 1

    if total_booked_overview > 0:
        overall_attendance_rate = round((total_attended_overview / total_booked_overview) * 100, 1)
    else:
        overall_attendance_rate = 0

    participants = (db.session.query(Attendance.UserId)
                    .filter(Attendance.AttendanceStatus == "Attended")
                    .distinct()
                    .count()
                    )
    
    attendees_per_session = []

    no_shows = []
    no_show_rate = 0
    total_no_show = 0
    total_booked_all = 0

    topic_counts = defaultdict(int)
    learner_history = defaultdict(int)

    upcoming_bookings = []

    for sess in normal_sessions:
        if sess.Status != "Completed":
            continue
        session_attendees = 0
        for booking in sess.bookings:
            if booking.Status in ['Approved', 'Completed']:
                total_booked_all += 1
                if sess.Status != "Completed":
                    upcoming_bookings.append(booking)
                if booking.attendance:
                    if booking.attendance.AttendanceStatus == "Attended":
                        session_attendees += 1
                        learner_history[booking.UserId] += 1
                    elif booking.attendance.AttendanceStatus == "Absent":
                        total_no_show += 1
                        no_shows.append({
                            "FirstName": booking.user.FirstName,
                            "LastName": booking.user.LastName,
                            "JobTitle": booking.user.JobTitle,
                            "SessionTitle": sess.Title
                        })
            if sess:
                topic_counts[sess.Title] += 1
            else:
                topic_counts["Unknown Course"] += 1
            
        attendees_per_session.append({
            "title": sess.Title,
            "count": session_attendees
        })
    
    no_show_rate = round((total_no_show / total_booked_all) * 100, 1) if total_booked_all else 0

    most_popular_topics = sorted(topic_counts.items(), key=lambda x:x[1], reverse=True)[:5]

    learner_participation = sorted(learner_history.items(), key=lambda x: x[1], reverse=True)[:5]


    chart_data = {
        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
        "values": [12, 19, 8, 15, 22]
    }    



    return render_template(
        'reports_and_analytics.html',
        admin=admin,
        users=users,
        tab=tab,
        sessions=normal_sessions,
        bookings=bookings,
        attendance_rate=attendance_rate,
        overall_attendance_rate=overall_attendance_rate,
        upcoming_bookings=upcoming_bookings,
        participants=participants,
        attendees_per_session=attendees_per_session,
        most_popular_topics=most_popular_topics,
        no_show_rate=no_show_rate,
        no_shows=no_shows,
        learner_participation=learner_participation,
        chart_data=chart_data
        )