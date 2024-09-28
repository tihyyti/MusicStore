from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
from datetime import datetime
from __init__ import db, logger

store_manager_bp = Blueprint('store_manager', __name__)

@store_manager_bp.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        storeManagerName = request.form['storeManagerName']
        storeManagerPassw = request.form['storeManagerPassw']

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, storeManagerPassw FROM mstore_v1.Store WHERE storeManagerName = %s",
            (storeManagerName,),
        )
        storemanager = cur.fetchone()

        if storemanager is not None:
            if storemanager and bcrypt.checkpw(storeManagerPassw.encode('utf-8'), storemanager[1].  encode('utf-8')):
                session['storemanager'] = storemanager[0]
                cur.execute(
                    "UPDATE mstore_v1.Store SET last_login = %s WHERE id = %s",
                    (datetime.now(), storemanager[0]),
                )
                conn.commit()
                cur.close()
                conn.close()
                flash('Login successful!', 'success')
                return redirect(url_for('mainmenu.mainmenu'))
            else:
                cur.close()
                conn.close()
                flash('Invalid username or password.', 'danger')
                logger.error('Store Manager not found')
                return redirect(url_for("mainmenu.mainmenu"))
        else:
            flash('No store manager record in the system !.', 'danger')
            logger.error('Customer not found')

    return render_template('login_manager.html')

@store_manager_bp.route('/manager_dashboard')
def manager_dashboard():
    if 'manager_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()

        # Fetch KPIs
        # cur.execute("SELECT total_sales FROM TotalSales")
        # total_sales = cur.fetchone()[0]

        # cur.execute("SELECT total_profit FROM TotalProfit")
        # total_profit = cur.fetchone()[0]

        # cur.execute("SELECT total_discounts FROM TotalDiscounts")
        # total_discounts = cur.fetchone()[0]

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
