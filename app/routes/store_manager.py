from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
from datetime import datetime

store_manager_bp = Blueprint('store_manager', __name__)

@store_manager_bp.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        storeManagerName = request.form['storeManagerName']
        storeManagerPssw = request.form['storeManagerPssw']

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, storeManagerPssw FROM Store WHERE storeManagerName = %s", (storeManagerName,))
        manager = cur.fetchone()

        if manager and bcrypt.checkpw(storeManagerPssw.encode('utf-8'), manager[1].encode('utf-8')):
            session['manager_id'] = manager[0]
            cur.execute("UPDATE Store SET last_login = %s WHERE id = %s", (datetime.now(), manager[0]))
            conn.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('store_manager.manager_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

        cur.close()
        conn.close()

    return render_template('login_manager.html')

@store_manager_bp.route('/manager_dashboard')
def manager_dashboard():
    if 'manager_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()

        # Fetch KPIs
        cur.execute("SELECT total_sales FROM TotalSales")
        total_sales = cur.fetchone()[0]

        cur.execute("SELECT total_profit FROM TotalProfit")
        total_profit = cur.fetchone()[0]

        cur.execute("SELECT total_discounts FROM TotalDiscounts")
        total_discounts = cur.fetchone()[0]

        cur.close()
        conn.close()

        return render_template('manager_dashboard.html', total_sales=total_sales, total_profit=total_profit, total_discounts=total_discounts)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

@store_manager_bp.route('/report/<report_name>')
def report(report_name):
    if 'manager_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM {report_name}"
        cur.execute(query)
        report_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('report.html', report_name=report_name, report_data=report_data)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

@store_manager_bp.route('/basic_listing/<listing_name>')
def basic_listing(listing_name):
    if 'manager_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM {listing_name}"
        cur.execute(query)
        listing_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('basic_listing.html', listing_name=listing_name, listing_data=listing_data)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

@store_manager_bp.route('/logout_manager')
def logout_manager():
    session.pop('manager_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('store_manager.login_manager'))
