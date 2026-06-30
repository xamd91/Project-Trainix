from flask import render_template, session, redirect, url_for, request
from models import Users, TrainingSessions, Bookings, Departments, TrainingCourses, Attendance
from sqlalchemy import func, or_, extract, case
from app import db
from collections import defaultdict

MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

FUNNEL_COLORS = {
    'Completed': '#10b981',
    'Approved': '#00B0C2',
    'Pending Approval': '#F99D20',
    'Cancelled': '#f97316',
    'Rejected': '#ef4444',
}

def page():

    # ── STAT CARDS ────────────────────────────────────────────────────────
    total_sessions = (
        db.session.query(func.count(TrainingSessions.SessionId))
        .filter(TrainingSessions.Status == "Completed")
        .scalar()
    ) or 0
    
    total_bookings = db.session.query(func.count(Bookings.BookingId)).scalar() or 0

    # Attendance rate — Attended vs (Attended + Absent), completed sessions only
    attendance_counts = (
        db.session.query(Attendance.AttendanceStatus, func.count(Attendance.AttendanceId))
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .filter(TrainingSessions.Status == 'Completed')
        .group_by(Attendance.AttendanceStatus)
        .all()
    )
    att_counts = {status: count for status, count in attendance_counts}
    attended = att_counts.get('Attended', 0)
    absent = att_counts.get('Absent', 0)
    marked_total = attended + absent
    overall_attendance_rate = round((attended / marked_total) * 100, 1) if marked_total else 0
    participants = attended

    # Booking completion rate — Completed / all decided (non-pending) bookings
    status_counts = (
        db.session.query(Bookings.Status, func.count(Bookings.BookingId))
        .group_by(Bookings.Status)
        .all()
    )
    b_counts = {status: count for status, count in status_counts}
    completed_bookings = b_counts.get('Completed', 0)
    decided_total = sum(v for k, v in b_counts.items() if k != 'Pending Approval')
    completion_rate = round((completed_bookings / decided_total) * 100, 1) if decided_total else 0

    # Avg seat fill rate — Booked / Capacity across sessions with capacity > 0
    capacity_rows = (
        db.session.query(TrainingSessions.Booked, TrainingSessions.Capacity)
        .filter(TrainingSessions.Capacity > 0)
        .all()
    )
    if capacity_rows:
        avg_fill_rate = round(
            sum((booked or 0) / cap for booked, cap in capacity_rows) / len(capacity_rows) * 100, 1
        )
    else:
        avg_fill_rate = 0

    # ── CHART: SESSIONS BY MONTH ─────────────────────────────────────────
    month_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            func.count(TrainingSessions.SessionId)
        )
        .group_by('month')
        .order_by('month')
        .all()
    )
    month_counts = {int(m): c for m, c in month_rows}
    sessions_by_month = {
        'labels': [MONTH_LABELS[i - 1] for i in sorted(month_counts)],
        'data': [month_counts[i] for i in sorted(month_counts)],
    }

    # ── CHART: SESSIONS BY DEPARTMENT ─────────────────────────────────────
    dept_session_rows = (
        db.session.query(Departments.DepartmentName, func.count(TrainingSessions.SessionId))
        .join(TrainingCourses, TrainingCourses.DepartmentId == Departments.DepartmentId)
        .join(TrainingSessions, TrainingSessions.CourseId == TrainingCourses.CourseId)
        .group_by(Departments.DepartmentName)
        .all()
    )
    sessions_by_dept = {
        'labels': [r[0] for r in dept_session_rows],
        'data': [r[1] for r in dept_session_rows],
    }

    # ── CHART: ATTENDANCE TREND (line, % per month) ───────────────────────
    trend_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            Attendance.AttendanceStatus,
            func.count(Attendance.AttendanceId)
        )
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .group_by('month', Attendance.AttendanceStatus)
        .order_by('month')
        .all()
    )
    trend_monthly = defaultdict(lambda: {'Attended': 0, 'Absent': 0})
    for month, status, count in trend_rows:
        if status in ('Attended', 'Absent'):
            trend_monthly[int(month)][status] = count

    trend_months_sorted = sorted(trend_monthly.keys())
    attendance_trend = {
        'labels': [MONTH_LABELS[m - 1] for m in trend_months_sorted],
        'data': [
            round((trend_monthly[m]['Attended'] /
                   (trend_monthly[m]['Attended'] + trend_monthly[m]['Absent'])) * 100, 1)
            if (trend_monthly[m]['Attended'] + trend_monthly[m]['Absent']) else 0
            for m in trend_months_sorted
        ],
    }

    # ── CHART: DELIVERY TYPE SPLIT ─────────────────────────────────────────
    delivery_rows = (
        db.session.query(TrainingSessions.DeliveryType, func.count(TrainingSessions.SessionId))
        .group_by(TrainingSessions.DeliveryType)
        .all()
    )
    delivery_counts = {dtype: count for dtype, count in delivery_rows}
    delivery_split = {
        'labels': ['Face-to-Face', 'Online'],
        'data': [delivery_counts.get('Face-to-Face', 0), delivery_counts.get('Online', 0)],
    }

    # ── CHART: ATTENDANCE STACK BY MONTH ───────────────────────────────────
    stack_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            Attendance.AttendanceStatus,
            func.count(Attendance.AttendanceId)
        )
        .join(Bookings, Attendance.BookingId == Bookings.BookingId)
        .join(TrainingSessions, Bookings.SessionId == TrainingSessions.SessionId)
        .group_by('month', Attendance.AttendanceStatus)
        .order_by('month')
        .all()
    )
    stack_monthly = defaultdict(lambda: {'Attended': 0, 'Absent': 0, 'N/A': 0})
    for month, status, count in stack_rows:
        stack_monthly[int(month)][status] = count

    stack_months_sorted = sorted(stack_monthly.keys())
    attendance_stack = {
        'labels': [MONTH_LABELS[m - 1] for m in stack_months_sorted],
        'attended': [stack_monthly[m]['Attended'] for m in stack_months_sorted],
        'absent': [stack_monthly[m]['Absent'] for m in stack_months_sorted],
        'na': [stack_monthly[m]['N/A'] for m in stack_months_sorted],
    }

    # ── CHART: OVERALL ATTENDANCE BREAKDOWN (doughnut) ────────────────────
    pie_rows = (
        db.session.query(Attendance.AttendanceStatus, func.count(Attendance.AttendanceId))
        .group_by(Attendance.AttendanceStatus)
        .all()
    )
    pie_counts = {status: count for status, count in pie_rows}
    attendance_pie = {
        'attended': pie_counts.get('Attended', 0),
        'absent': pie_counts.get('Absent', 0),
        'na': pie_counts.get('N/A', 0),
    }

    # ── BOOKING FUNNEL ──────────────────────────────────────────────────
    funnel_rows = (
        db.session.query(Bookings.Status, func.count(Bookings.BookingId))
        .group_by(Bookings.Status)
        .all()
    )
    funnel_counts = {status: count for status, count in funnel_rows}
    booking_funnel = [
        {'label': label, 'count': funnel_counts.get(label, 0), 'color': color}
        for label, color in FUNNEL_COLORS.items()
    ]

    # ── CHART: BOOKING STATUS STACK BY MONTH (by BookingDate) ─────────────
    booking_stack_rows = (
        db.session.query(
            extract('month', Bookings.BookingDate).label('month'),
            Bookings.Status,
            func.count(Bookings.BookingId)
        )
        .group_by('month', Bookings.Status)
        .order_by('month')
        .all()
    )
    booking_stack_monthly = defaultdict(
        lambda: {'Completed': 0, 'Approved': 0, 'Cancelled': 0, 'Rejected': 0, 'Pending Approval': 0}
    )
    for month, status, count in booking_stack_rows:
        if status in booking_stack_monthly[int(month)]:
            booking_stack_monthly[int(month)][status] = count

    booking_months_sorted = sorted(booking_stack_monthly.keys())
    booking_status_stack = {
        'labels': [MONTH_LABELS[m - 1] for m in booking_months_sorted],
        'approved': [booking_stack_monthly[m]['Approved'] for m in booking_months_sorted],
        'completed': [booking_stack_monthly[m]['Completed'] for m in booking_months_sorted],
        'cancelled': [booking_stack_monthly[m]['Cancelled'] for m in booking_months_sorted],
        'rejected': [booking_stack_monthly[m]['Rejected'] for m in booking_months_sorted],
        'pending': [booking_stack_monthly[m]['Pending Approval'] for m in booking_months_sorted],
    }

    # ── FILL RATE — SESSION LIST ──────────────────────────────────────────
    fill_rows = (
        db.session.query(TrainingSessions, TrainingCourses.CourseName, Departments.DepartmentName)
        .join(TrainingCourses, TrainingSessions.CourseId == TrainingCourses.CourseId)
        .outerjoin(Departments, TrainingCourses.DepartmentId == Departments.DepartmentId)
        .filter(TrainingSessions.Capacity > 0)
        .all()
    )
    fill_rate_sessions = []
    for sess, course_name, dept_name in fill_rows:
        booked = sess.Booked or 0
        fill_rate_sessions.append({
            'title': course_name,
            'dept': dept_name or 'Unassigned',
            'booked': booked,
            'cap': sess.Capacity,
            '_fill_pct': booked / sess.Capacity,
        })
    # lowest fill first — surfaces at-risk sessions; flip reverse=True to show best fill first
    fill_rate_sessions.sort(key=lambda s: s['_fill_pct'])
    for s in fill_rate_sessions:
        del s['_fill_pct']
    fill_rate_sessions = fill_rate_sessions[:6]

    # ── FILL RATE TREND (line, % per month) ────────────────────────────
    fill_trend_rows = (
        db.session.query(
            extract('month', TrainingSessions.Date).label('month'),
            TrainingSessions.Booked,
            TrainingSessions.Capacity
        )
        .filter(TrainingSessions.Capacity > 0)
        .all()
    )
    fill_trend_monthly = defaultdict(list)
    for month, booked, cap in fill_trend_rows:
        fill_trend_monthly[int(month)].append((booked or 0) / cap)

    fill_trend_months_sorted = sorted(fill_trend_monthly.keys())
    fill_rate_trend = {
        'labels': [MONTH_LABELS[m - 1] for m in fill_trend_months_sorted],
        'data': [
            round(sum(fill_trend_monthly[m]) / len(fill_trend_monthly[m]) * 100, 1)
            for m in fill_trend_months_sorted
        ],
    }

    # ── DEPARTMENT ATTENDED (polar area) ──────────────────────────────────
    dept_attended_rows = (
        db.session.query(Departments.DepartmentName, func.count(Attendance.AttendanceId))
        .join(Users, Users.DepartmentId == Departments.DepartmentId)
        .join(Attendance, Attendance.UserId == Users.UserId)
        .filter(Attendance.AttendanceStatus == 'Attended')
        .group_by(Departments.DepartmentName)
        .all()
    )
    dept_attended = {
        'labels': [r[0] for r in dept_attended_rows],
        'data': [r[1] for r in dept_attended_rows],
    }

    # ── RANKINGS: TRAINERS ────────────────────────────────────────────────
    trainer_rows = (
        db.session.query(
            Users.UserId, Users.FirstName, Users.LastName,
            func.count(func.distinct(TrainingSessions.SessionId)).label('sessions_count'),
            func.sum(case((Attendance.AttendanceStatus == 'Attended', 1), else_=0)).label('attended'),
            func.sum(case((Attendance.AttendanceStatus.in_(['Attended', 'Absent']), 1), else_=0)).label('marked'),
        )
        .join(TrainingSessions, TrainingSessions.TrainerId == Users.UserId)
        .join(Bookings, Bookings.SessionId == TrainingSessions.SessionId)
        .join(Attendance, Attendance.BookingId == Bookings.BookingId)
        .filter(Users.Role == 'Trainer')
        .group_by(Users.UserId, Users.FirstName, Users.LastName)
        .all()
    )
    trainers_ranked = []
    for uid, fname, lname, sessions_count, attended_n, marked_n in trainer_rows:
        rate = round((attended_n / marked_n) * 100) if marked_n else 0
        trainers_ranked.append({
            'name': f"{fname} {lname}",
            'sub': f"{sessions_count} session{'s' if sessions_count != 1 else ''} delivered",
            'metric_num': f"{rate}%",
            'metric_lbl': 'attendance rate',
            '_rate': rate,
        })
    trainers_ranked.sort(key=lambda t: t['_rate'], reverse=True)
    for t in trainers_ranked:
        del t['_rate']
    top_trainers = trainers_ranked[:3]
    bottom_trainers = trainers_ranked[-3:][::-1] if len(trainers_ranked) > 3 else []

    # ── RANKINGS: SESSIONS ────────────────────────────────────────────────
    session_rows = (
        db.session.query(
            TrainingSessions.SessionId, TrainingCourses.CourseName, Departments.DepartmentName,
            func.sum(case((Attendance.AttendanceStatus == 'Attended', 1), else_=0)).label('attended'),
            func.sum(case((Attendance.AttendanceStatus.in_(['Attended', 'Absent']), 1), else_=0)).label('marked'),
        )
        .join(TrainingCourses, TrainingSessions.CourseId == TrainingCourses.CourseId)
        .outerjoin(Departments, TrainingCourses.DepartmentId == Departments.DepartmentId)
        .join(Bookings, Bookings.SessionId == TrainingSessions.SessionId)
        .join(Attendance, Attendance.BookingId == Bookings.BookingId)
        .group_by(TrainingSessions.SessionId, TrainingCourses.CourseName, Departments.DepartmentName)
        .all()
    )
    sessions_ranked = []
    for sid, cname, dname, attended_n, marked_n in session_rows:
        if not marked_n:
            continue
        rate = round((attended_n / marked_n) * 100)
        sessions_ranked.append({
            'name': cname,
            'sub': f"{dname or 'Unassigned'} · {attended_n} attended",
            'metric_num': f"{rate}%",
            'metric_lbl': 'attendance rate',
            '_rate': rate,
        })
    sessions_ranked.sort(key=lambda s: s['_rate'], reverse=True)
    for s in sessions_ranked:
        del s['_rate']
    top_sessions = sessions_ranked[:3]
    bottom_sessions = sessions_ranked[-3:][::-1] if len(sessions_ranked) > 3 else []

    # ── RANKINGS: COURSES ─────────────────────────────────────────────────
    course_rows = (
        db.session.query(
            TrainingCourses.CourseId, TrainingCourses.CourseName, Departments.DepartmentName,
            func.count(func.distinct(TrainingSessions.SessionId)).label('session_count'),
            func.sum(case((Attendance.AttendanceStatus == 'Attended', 1), else_=0)).label('attended'),
        )
        .outerjoin(Departments, TrainingCourses.DepartmentId == Departments.DepartmentId)
        .join(TrainingSessions, TrainingSessions.CourseId == TrainingCourses.CourseId)
        .join(Bookings, Bookings.SessionId == TrainingSessions.SessionId)
        .join(Attendance, Attendance.BookingId == Bookings.BookingId)
        .group_by(TrainingCourses.CourseId, TrainingCourses.CourseName, Departments.DepartmentName)
        .all()
    )
    courses_ranked = []
    for cid, cname, dname, session_count, attended_n in course_rows:
        attended_n = attended_n or 0
        courses_ranked.append({
            'name': cname,
            'sub': f"{session_count} session{'s' if session_count != 1 else ''} · {dname or 'Unassigned'}",
            'metric_num': str(attended_n),
            'metric_lbl': 'attended',
            '_attended': attended_n,
        })
    courses_ranked.sort(key=lambda c: c['_attended'], reverse=True)
    for c in courses_ranked:
        del c['_attended']
    top_courses = courses_ranked[:3]
    bottom_courses = courses_ranked[-3:][::-1] if len(courses_ranked) > 3 else []

    # ── RANKINGS: LEARNERS ────────────────────────────────────────────────
    learner_rows = (
        db.session.query(
            Users.UserId, Users.FirstName, Users.LastName, Departments.DepartmentName,
            func.sum(case((Attendance.AttendanceStatus == 'Attended', 1), else_=0)).label('attended'),
        )
        .outerjoin(Departments, Users.DepartmentId == Departments.DepartmentId)
        .join(Bookings, Bookings.UserId == Users.UserId)
        .join(Attendance, Attendance.BookingId == Bookings.BookingId)
        .filter(Users.Role == 'Learner')
        .group_by(Users.UserId, Users.FirstName, Users.LastName, Departments.DepartmentName)
        .all()
    )
    learners_ranked = []
    for uid, fname, lname, dname, attended_n in learner_rows:
        attended_n = attended_n or 0
        learners_ranked.append({
            'name': f"{fname} {lname}",
            'sub': f"{dname or 'Unassigned'} · {attended_n} session{'s' if attended_n != 1 else ''} attended",
            'metric_num': str(attended_n),
            'metric_lbl': 'attended',
            '_attended': attended_n,
        })
    learners_ranked.sort(key=lambda l: l['_attended'], reverse=True)
    for l in learners_ranked:
        del l['_attended']
    top_learners = learners_ranked[:3]
    bottom_learners = learners_ranked[-3:][::-1] if len(learners_ranked) > 3 else []

    # ── ASSEMBLE chart_data FOR THE TEMPLATE / JS ──────────────────────────
    chart_data = {
        'sessions_by_month': sessions_by_month,
        'sessions_by_dept': sessions_by_dept,
        'attendance_trend': attendance_trend,
        'delivery_split': delivery_split,
        'attendance_stack': attendance_stack,
        'attendance_pie': attendance_pie,
        'booking_funnel': booking_funnel,
        'booking_status_stack': booking_status_stack,
        'fill_rate_sessions': fill_rate_sessions,
        'fill_rate_trend': fill_rate_trend,
        'dept_attended': dept_attended,
        'rankings': {
            'top_trainers': top_trainers,
            'bottom_trainers': bottom_trainers,
            'top_sessions': top_sessions,
            'bottom_sessions': bottom_sessions,
            'top_courses': top_courses,
            'bottom_courses': bottom_courses,
            'top_learners': top_learners,
            'bottom_learners': bottom_learners,
        },
    }   

    print(chart_data['attendance_trend'])

    return render_template(
        'reports_and_analytics.html',
        total_sessions=total_sessions,
        total_bookings=total_bookings,
        overall_attendance_rate=overall_attendance_rate,
        participants=participants,
        completion_rate=completion_rate,
        avg_fill_rate=avg_fill_rate,
        chart_data=chart_data,
    )