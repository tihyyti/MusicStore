from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import bcrypt
import psycopg2
from datetime import datetime
from __init__ import db, logger


customerregist_bp = Blueprint('register_customer', __name__)

bcrypt = Bcrypt()
@customerregist_bp.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    if request.method == 'POST':
        custoName = request.form['custoName']
        custoPassw = request.form['custoPassw']
        custoEmail = request.form.get('custoEmail')
        custoPhone = request.form.get('custoPhone')
        custoStatus = False
        custoBlocked = False

        # Hash the password
        custoPsw = bcrypt.generate_password_hash(custoPassw).decode('utf-8')

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        logger.debug('db connected')

        try:
            # last_login = datetime.now()
            cur.execute(
                """
                INSERT INTO mstore_v1.Customer (store_id, custoName, custoEmail, custoPhone, custoStatus, custoBlocked, last_login, custoPassw)
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    1,
                    custoName,
                    custoEmail,
                    custoPhone,
                    custoStatus,
                    custoBlocked,
                    datetime.now(),
                    custoPsw,
                ),
            )
            conn.commit()
            logger.debug("db committed successfully")
            flash('Customer registration successful!', 'success')

        except psycopg2.IntegrityError:
            conn.rollback()
            cur.close()
            conn.close()
            flash('Username or password already exists.', 'danger')

        finally:
            cur.close()
            conn.close()
            return redirect(url_for('mainmenu.mainmenu'))

    return render_template('register_customer.html')

if __name__ == '__main__':
    app.run(debug=True)
