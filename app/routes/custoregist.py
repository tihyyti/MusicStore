
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
import psycopg2
from __init__ import db, logger

custoregist_bp = Blueprint('register', __name__)
@custoregist_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        custoName = request.form['custoName']
        custoPassw = request.form['custoPassw']
        custoEmail = request.form.get('custoEmail')
        custoPhone = request.form.get('custoPhone')
        custoStatus = False
        custoBlocked = False

        hashed_passw = bcrypt.hashpw(custoPassw.encode('utf-8'), bcrypt.gensalt())

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        logger.debug('db connected')
        try:
            cur.execute("""
                INSERT INTO Customer (Store_id, custoName, custoPassw, custoEmail, custoPhone, custoStatus, custoBlocked)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (1, custoName, hashed_passw, custoEmail, custoPhone, custoStatus, custoBlocked))
            conn.commit()
            flash('Registration successful!', 'success')
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Username or password already exists.', 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('register'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)