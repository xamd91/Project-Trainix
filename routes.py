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
        return render_template('admin_dashboard.html')

    @app.route('/attendance_management', methods=['GET','POST'])
    def attendance_management():
        from pages.attendance_management import page
        return page()
    
    @app.route('/mark_attendance', methods=["POST"])
    def mark_attendance_route():
        from pages.mark_attendance_page import mark_attendance
        return mark_attendance()

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

    @app.route('/reports', methods=['GET','POST'])
    def reports():
        return render_template('reports.html')

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
