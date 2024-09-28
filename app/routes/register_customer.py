from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import psycopg2
from datetime import datetime
from __init__ import db, logger

customerregist_bp = Blueprint("register_customer", __name__)

bcrypt = Bcrypt()
@customerregist_bp.route("/register_customer", methods=["GET", "POST"])
def register_customer():
    if request.method == "POST":
        custoName = request.form['custoName']
        custoPassw = request.form['custoPassw']
        custoEmail = request.form.get('custoEmail')
        custoPhone = request.form.get('custoPhone')
        custoStatus = False
        custoBlocked = False
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
