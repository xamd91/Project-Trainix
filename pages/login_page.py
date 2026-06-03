import re
from flask import request, render_template, session, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users
from app import db

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

        user = Users.query.filter_by(Email=email).first()

        if user and check_password_hash(user.Password, password):

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

                return jsonify({
                    "status": "success",
                    "message": f"Welcome back {user.FirstName}.",
                    "role": 'manager'
                }), 201

            elif user.Role == 'Admin':
                session['role'] = 'admin'

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

        return jsonify({
            "status": "error",
            "message": "Invalid email or password."
        }), 400

    return render_template("login.html")