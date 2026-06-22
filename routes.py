import os
from flask import session, render_template, request, redirect, url_for, jsonify
from models import Users
from app import db

def register_routes(app, db):

    @app.route('/account', methods=['GET','POST'])
    def account():
        from pages.account import page
        return page()

    @app.route('/admin_dashboard', methods=['GET','POST'])
    def admin_dashboard():
        from pages.admin_dashboard import page
        return page()

    @app.route('/admin_dashboard/create_user', methods=['GET','POST'])
    def create_user_route():
        from pages.create_user import create_user
        return create_user()

    @app.route('/admin_dashboard/edit_user/<int:user_id>', methods=['GET','POST'])
    def edit_user_route(user_id):
        from pages.edit_user import edit_user
        return edit_user(user_id)
    
    @app.route('/admin_dashboard/delete_user/<int:user_id>', methods=['GET','POST'])
    def delete_user_route(user_id):
        from pages.delete_user import delete_user
        return delete_user(user_id)

    @app.route('/admin_dashboard/create_session', methods=['GET','POST'])
    def create_session_route():
        from pages.create_session import create_session
        return create_session()
    
    @app.route('/admin_dashboard/edit_session/<int:session_id>', methods=['GET','POST'])
    def edit_session_route(session_id):
        from pages.edit_session import edit_session
        return edit_session(session_id)
    
    @app.route('/admin_dashboard/delete_session/<int:session_id>', methods=['GET','POST'])
    def delete_session_route(session_id):
        from pages.delete_session import delete_session
        return delete_session(session_id)
    
    @app.route('/admin_dashboard/create_department', methods=['GET','POST'])
    def create_department_route():
        from pages.create_department import create_department
        return create_department()
    
    @app.route('/admin_dashboard/edit_department/<int:department_id>', methods=['GET','POST'])
    def edit_department_route(department_id):
        from pages.edit_department import edit_department
        return edit_department(department_id)

    @app.route('/admin_dashboard/delete_department/<int:department_id>', methods=['GET','POST'])
    def delete_department_route(department_id):
        from pages.delete_department import delete_department
        return delete_department(department_id)


    @app.route('/attendance_management', methods=['GET','POST'])
    def attendance_management():
        from pages.attendance_management import page
        return page()
    
    @app.route('/attendance_management/mark_attendance', methods=["POST"])
    def mark_attendance_route():
        from pages.mark_attendance_page import mark_attendance
        return mark_attendance()
    
    @app.route('/attendance_management/complete_session/<int:session_id>')
    def complete_session_route(session_id):
        from pages.complete_session import complete_session
        return complete_session(session_id) 
    
    @app.route('/account/cancel_booking/<int:booking_id>')
    def cancel_booking_route(booking_id):
        from pages.cancel_booking_page import cancel_booking
        return cancel_booking(booking_id)
    
    @app.route('/account/update_profile', methods=["POST"])
    def update_profile_route():
        from pages.update_profile import update_profile
        return update_profile()

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        from pages.login_page import page
        return page()
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
    
    @app.route('/manager_dashboard', methods=['GET','POST'])
    def manager_dashboard():
        from pages.manager_dashboard import page
        return page()

    @app.route('/reports_and_analytics', methods=['GET','POST'])
    def reports_and_analytics():
        from pages.reports import page
        return page()
    
    @app.route('/register', methods=["GET", "POST"])
    def register():
        from pages.register_page import page
        return page()

    @app.route('/training_catalogue')
    def training_catalogue():
        from pages.catalogue_page import page
        return page()

    @app.route('/training_details/<int:session_id>')
    def training_details(session_id):
        from pages.training_details_page import page
        return page(session_id) 

    @app.route('/book_session/<int:session_id>', methods=["POST"])
    def book_session_route(session_id):
        from pages.book_session_page import book_session
        return book_session(session_id)

    @app.route('/information_and_support')
    def information_and_support():
        return render_template('information_and_support.html')  

    @app.route("/db-test")
    def db_test():
        try:
            # db test
            result = db.session.execute(db.text("SELECT 1")).scalar()
            return jsonify({
                "status": "success",
                "db_response": result
            })
        except Exception as e:
            print(os.getenv("DATABASE_URL"))
            print("DB URL:", os.getenv("DATABASE_URL"))
            return jsonify({
                "status": "error",
                "message": str(e)
            })
