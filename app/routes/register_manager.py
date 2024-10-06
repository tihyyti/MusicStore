from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf import CSRFProtect
import psycopg2
from datetime import datetime
from __init__ import db, logger

managerregist_bp = Blueprint('register_manager', __name__)

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

@managerregist_bp.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        storeManagerName = bleach.clean(request.form['storeManagerName'])
        storeManagerPassw = bleach.clean(request.form['storeManagerPassw'])
        storeName = bleach.clean(request.form['storeName'])
        storeTaxId = bleach.clean(request.form['storeTaxId'])
        storePhone = bleach.clean(request.form['storePhone'])
        storeEmail = bleach.clean(request.form['storeEmail'])
        storeAddress = bleach.clean(request.form['storeAddress'])
        storeLogoUrl = bleach.clean(request.form.get('storeLogoUrl'))
        storeManager_id = bleach.clean(request.form["managers_customer_id"])

        # Validate the inputs:
        # Name Validation: Ensures the name contains only letters and spaces.
        is_name_valid = validate_name(storeManagerName)
        # Password Validation: Checks if the password is at least 8 characters long.
        is_password_valid = validate_password(storeManagerPassw)
        # Email Validation: Uses a regular expression to check for a valid email format.
        is_email_valid = validate_email(storeEmail)
        # Phone Validation: Ensures the phone number is between 10 to 15 digits and can include aleading ‘+’.
        is_phone_valid = validate_phone(storePhone)

        # Check all validations
        if is_name_valid and is_password_valid and is_email_valid and is_phone_valid:
            storeManagerStatus = True
        else:
            storeManagerStatus = False

        # Hash the password
        storeManagerPsw = bcrypt.generate_password_hash(storeManagerPassw).decode("utf-8")

        last_login = datetime.now()
        conn = None
        cur = None

        try:
            conn = db.engine.raw_connection()
            cur = conn.cursor()
            logger.debug('db connected')

            cur.execute(
                """
                INSERT INTO mstore_v1.Store (storeManagerName, storeName, storeTaxid,
                storePhone, storeEmail, storeAddress, storeLogoUrl, storeManager_id,
                last_login, storeManagerPassw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    storeManagerName,
                    storeName,
                    storeTaxId,
                    storePhone,
                    storeEmail,
                    storeAddress,
                    storeLogoUrl,
                    storeManager_id,
                    last_login,
                    storeManagerPsw,
                ),
            )
            conn.commit()
            logger.debug("db committed successfully")
            flash('Store Manager registration successful!', 'success')

        except psycopg2.IntegrityError as e:
            if conn:
                conn.rollback()
            logger.error(f"IntegrityError: {e}")
            flash('Store Manager registration failed. Please check your inputs.', 'danger')
            return redirect(url_for('register_manager.register_manager'))

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('mainmenu.mainmenu'))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
            return redirect(url_for('mainmenu.mainmenu'))

    return render_template('register_manager.html')
