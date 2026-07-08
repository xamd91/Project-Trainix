from flask import jsonify, redirect, url_for
from models import Departments
from app import db


def delete_department(department_id):

    department = Departments.query.get(department_id)

    if not department:
        return jsonify({
            "status": "error",
            "message": "Department not found."
        }), 404


    users = department.users

    if users:
        return jsonify({
            "status": "warning",
            "message": (
                f"The {department.DepartmentName} department currently has "
                f"at least one user assigned to it. Please change the user's "
                "department before proceeding."
            )
        }), 400


    courses = department.courses

    if courses:
        return jsonify({
            "status": "warning",
            "message": (
                f"The {department.DepartmentName} department currently has "
                f"at least one course assigned to it. Please change the "
                "course's department before proceeding."
            )
        }), 400

    if department.ManagerId:
        return jsonify({
            "status": "warning",
            "message": (
                f"The {department.DepartmentName} department currently has "
                "a manager assigned. Please remove the manager before deleting "
                "the department."
            )
        }), 400


    db.session.delete(department)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": f"{department.DepartmentName} department successfully deleted!"
    }), 200