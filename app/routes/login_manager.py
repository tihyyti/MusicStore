from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
from datetime import datetime
from __init__ import db, logger

login_manager_bp = Blueprint('login_manager', __name__)

@login_manager_bp.route('/manager_login', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        custoName = request.form['storeManagerName']
        custoPssw = request.form['storeManagerPssw']

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        logger.debug('db connected')

        cur.execute("SELECT id, storeManagerPssw FROM Store WHERE storeManagerName = %s", (storeManagerName,))
        storeManager = cur.fetchone()

        if storeManagerPssw and bcrypt.checkpw(storeManagerPssw.encode('utf-8'), storeManager[1].encode('utf-8')):
          #db.session['customer'] = customer[0]
          #cur.execute("UPDATE Customer SET last_login = %s WHERE id = %s", (datetime.now(), customer[0]))
          #conn.commit()
          cur.close()
          conn.close()
          flash('Login successful!', 'success')
          return redirect(url_for('manager_dashboard.manager_dashboard'))
        else:
          flash('Invalid username or password.', 'danger')
          cur.close()
          conn.close()
          return render_template('login_manager.html')
    return render_template('login_manager.html')
