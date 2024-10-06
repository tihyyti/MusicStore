from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf import CSRFProtect
import psycopg2
from datetime import datetime
from __init__ import db, logger

customerregist_bp = Blueprint("register_customer", __name__)

bcrypt = Bcrypt()

# Validation functions
def validate_name(name):
    return bool(re.match("^[A-Za-z\s]+$", name))
def validate_password(password):
    return len(password) >= 8
def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
def validate_phone(phone):
    return bool(re.match(r"^\+?\d{10,15}$", phone))

@customerregist_bp.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    if request.method == "POST":
        # Clean the input using bleach (sanitization)
        custoName = bleach.clean(request.form['custoName'])
        custoPassw = bleach.clean(request.form['custoPassw'])
        custoEmail = bleach.clean(request.form.get('custoEmail'))
        custoPhone = bleach.clean(request.form.get('custoPhone'))
        custoStatus = False
        custoBlocked = False

        # Validate the inputs:
        # Name Validation: Ensures the name contains only letters and spaces.
        is_name_valid = validate_name(custoName)
        # Password Validation: Checks if the password is at least 8 characters long.
        is_password_valid = validate_password(custoPassw)
        # Email Validation: Uses a regular expression to check for a valid email format.
        is_email_valid = validate_email(custoEmail)
        # Phone Validation: Ensures the phone number is between 10 to 15 digits and can include a leading ‘+’.
        is_phone_valid = validate_phone(custoPhone)

        # Check all validations
        if is_name_valid and is_password_valid and is_email_valid and is_phone_valid:
            custoStatus = True
        else:
            custoStatus = False

        # Output the validation results for input testing
        print(f"Name valid: {is_name_valid}")
        print(f"Password valid: {is_password_valid}")
        print(f"Email valid: {is_email_valid}")
        print(f"Phone valid: {is_phone_valid}")
        print(f"Overall status: {custoStatus}")

        # Hash the password
        custoPsw = bcrypt.generate_password_hash(custoPassw).decode("utf-8")
        last_login = datetime.now()
        conn = None
        cur = None

        # Check if email is already registered

        # Hash the password
        custoPsw = bcrypt.generate_password_hash(custoPassw).decode("utf-8")

        last_login = datetime.now()
        conn = None
        cur = None

        try:
            conn = db.engine.raw_connection()
            cur = conn.cursor()
            logger.debug("db connected")

            cur.execute(
            """
            INSERT INTO mstore_v1.Customer (store_id, custoName, custoEmail,
            custoPhone, custoStatus, custoBlocked, last_login, custoPassw)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                1,
                custoName,
                custoEmail,
                custoPhone,
                custoStatus,
                custoBlocked,
                last_login,
                custoPsw,
                ),
            )
            conn.commit()
            logger.debug("db committed successfully")
            flash('Customer registration successful!', 'success')

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error: {e}")
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("mainmenu.mainmenu"))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
            return redirect(url_for("mainmenu.mainmenu"))

    return render_template("register_customer.html")
