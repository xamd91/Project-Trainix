import re
from flask import request, render_template, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from app import db
from datetime import datetime, timedelta

def page():

    if 'user_id' in session:
        return redirect(url_for('home'))

    if request.method == "POST":

        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400

        # manager = Users.query.filter_by(Email=email).first()

        # if manager and check_password_hash(supplier.password, password):

        #     session['user_id'] = supplier.supplier_id
        #     session['role'] = 'supplier'

        #     return jsonify({
        #         "status": "success",
        #         "message": f"Welcome back Supplier - {supplier.name}.",
        #         "role": 'supplier'
        #     }), 201

        login_attempts = session.get('login_attempts', {})
        email_data = login_attempts.get(email, {'attempts': 0, 'lockout_until': None})

        if email_data['lockout_until']:
            lockout_until = datetime.fromisoformat(email_data['lockout_until'])
            if datetime.now() < lockout_until:
                remaining = int((lockout_until - datetime.now()).total_seconds())
                return jsonify({
                    "status": "error",
                    "message": f"Too many failed attempts for this accunt. Try again in {remaining} seconds."
                }), 429
            else:
                email_data = {'attempts': 0, 'lockout_until': None}

        user = Users.query.filter_by(Email=email).first()

        if user and check_password_hash(user.Password, password):

            login_attempts.pop(email, None)
            session['login_attemtps'] = login_attempts

            session['user_id'] = user.UserId

            if user.Role == "Learner":
                session['role'] = 'learner'

                return jsonify({
                    "status": "success",
                    "message": f"Welcome back {user.FirstName}.",
                    "role": 'learner'
                }), 201

            elif user.Role == "Trainer":
                session['role'] = 'trainer'

                return jsonify({
                    "status": "success",
                    "message": f"Welcome back {user.FirstName}.",
                    "role": 'trainer'
                }), 201

            elif user.Role == 'Manager':
                session['role'] = 'manager'

                if user.TrainerPerms == 'Yes':
                    session['trainer_perms'] = True

                if user.AdminPerms == 'Yes':
                    session['admin_perms'] = True

                return jsonify({
                    "status": "success",
                    "message": f"Welcome back {user.FirstName}.",
                    "role": 'manager'
                }), 201

            elif user.Role == 'Admin':
                session['role'] = 'admin'

                if user.TrainerPerms == 'Yes':
                    session['trainer_perms'] = True
                
                if user.ManagerPerms == "Yes":
                    session['manager_perms'] = True

                return jsonify({
                    "status": "success",
                    "message": f"Welcome back {user.FirstName}.",
                    "role": 'admin'
                }), 201
            
            else:
                session['role'] = 'undefined'
                # return jsonify({
                #     "status": "success",
                #     "message": f"Welcome back {user.firstname}.",
                #     "role": 'customer'
                # }), 201
        
        email_data['attempts'] += 1

        if email_data['attempts'] >= 5:
            email_data['lockout_until'] = (datetime.now() + timedelta(minutes=5)).isoformat()
            email_data['attmepts'] = 0
            login_attempts[email] = email_data
            session['login_attempts'] = login_attempts
            return jsonify({
                "status": "error",
                "message": "Too many failed attempts. This account is locked for 5 minutes."
            }), 429
        
        remaining_attempts = 5 - email_data['attempts']
        login_attempts[email] = email_data
        session['login_attempts'] = login_attempts

        return jsonify({
            "status": "error",
            "message": f"Invalid email or password. {remaining_attempts} attempt{'s' if remaining_attempts != 1 else ''} remaining."
        }), 400
        

    return render_template("login.html")