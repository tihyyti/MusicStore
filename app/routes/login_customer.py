from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
from datetime import datetime
from __init__ import db, logger

login_customer_bp = Blueprint('login_customer', __name__)

@login_customer_bp.route('/login', methods=['GET', 'POST'])
def login_customer():
    if request.method == 'POST':
        custoName = request.form['custoName']
        custoPassw = request.form['custoPassw']

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        logger.debug('db connected')

        cur.execute("SELECT id, custoPassw FROM Customer WHERE custoName = %s", (custoName,))
        customer = cur.fetchone()

        if custoPassw and bcrypt.checkpw(custoPassw.encode('utf-8'), customer[1].encode('utf-8')):
          #db.session['customer'] = customer[0]
          #cur.execute("UPDATE Customer SET last_login = %s WHERE id = %s", (datetime.now(), customer[0]))
          #conn.commit()
          cur.close()
          conn.close()
          flash('Login successful!', 'success')
          return redirect(url_for('customer_dashboard.customer_dashboard'))
        else:
          flash('Invalid username or password.', 'danger')
          cur.close()
          conn.close()
          return render_template('login_customer.html')
    return render_template('login_customer.html')
