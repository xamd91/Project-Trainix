from flask import render_template, request, redirect, url_for, jsonify
from app import db

def register_routes(app):

    @app.route('/account')
    def account():
        return render_template('account.html')

    @app.route('/admin_dashboard')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    @app.route('/attendance_management')
    def attendance_management():
        return render_template('attendance_management.html')

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login')
    def login():
        return render_template('login.html')
    
    @app.route('/manager_dashboard')
    def manager_dashboard():
        return render_template('manager_dashboard.html')

    @app.route('/reports')
    def reports():
        return render_template('reports.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    @app.route('/training_catalogue')
    def training_catalogue():
        return render_template('training_catalogue.html')

    @app.route('/training_details')
    def training_details():
        return render_template('training_details.html')    

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
            return jsonify({
                "status": "error",
                "message": str(e)
            })
