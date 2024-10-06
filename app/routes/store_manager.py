from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from __init__ import db, logger

store_manager_bp = Blueprint('store_manager', __name__)

# Validation functions
def validate_name(name):
    return bool(re.match("^[A-Za-z\s]+$", name))
def validate_password(password):
    return len(password) >= 8

@store_manager_bp.route('/login_manager', methods=['GET', 'POST'])
def login_manager():
    if request.method == 'POST':
        storeManagerName = bleach.clean(request.form['storeManagerName'])
        storeManagerPassw = bleach.clean(request.form['storeManagerPassw'])

        # Validate the inputs:
        is_name_valid = validate_name(storeManagerName)
        is_password_valid = validate_password(storeManagerPassw)

        # Check all validations
        storeManagerStatus = is_name_valid and is_password_valid

        # Output the validation results for input testing
        print(f"Name valid: {is_name_valid}")
        print(f"Password valid: {is_password_valid}")

        try:
            conn = db.engine.raw_connection()
            cur = conn.cursor()
            logger.debug('db connected')
            cur.execute(
                "SELECT id, storeManagerPassw FROM mstore_v1.Store WHERE storeManagerName = %s",
                (storeManagerName,),
            )
            storemanager = cur.fetchone()

            if storemanager:
                manager_id, stored_passw = storemanager  # tuple unpacking
                if storeManagerStatus and bcrypt.checkpw(storeManagerPassw.encode('utf-8'), stored_passw.encode('utf-8')):
                    session['manager_id'] = manager_id
                    cur.execute(
                        "UPDATE mstore_v1.Store SET last_login = %s WHERE id = %s",
                        (datetime.now(), manager_id),
                    )
                    conn.commit()
                    flash('Login successful!', 'success')
                    return redirect(url_for('mainmenu.mainmenu'))
                else:
                    if not is_name_valid and not is_password_valid:
                        flash('Invalid username and password.', 'danger')
                    elif not is_name_valid:
                        flash('Invalid username.', 'danger')
                    else:
                        flash('Invalid password.', 'danger')
                    logger.error('Store Manager not found, wrong credentials')
                    return redirect(url_for("mainmenu.mainmenu"))
            else:
                flash('No store manager record in the system!', 'danger')
                logger.error('Store Manager not found, wrong credentials')
                return redirect(url_for("mainmenu.mainmenu"))

        except Exception as e:
            logger.error(f'Error during login: {e}')
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for("mainmenu.mainmenu"))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('login_manager.html')

@store_manager_bp.route('/manager_dashboard')
def manager_dashboard():
    conn = db.engine.raw_connection()
    cur = conn.cursor()

    try:
        total_sales = 0.0
        total_discount = 0.0
        total_vat = 0.0

        customer_id = session.get('storemanager_id')

        if customer_id:
            cur.execute("SELECT id, custoName FROM mstore_v1.customer WHERE id = %s", (customer_id,))
            customer = cur.fetchone()

            if customer:
                customer_id, customer_name = customer
                print(f"Customer ID: {customer_id}, Customer Name: {customer_name}")

                # Fetch aggregated KPIs per customer
                cur.execute('''
                    SELECT
                        SUM(carttotal) AS total_sales,
                        SUM(cartdiscount) AS total_discount,
                        SUM(cartvat) AS total_vat
                    FROM mstore_v1.ShoppingCart
                    WHERE cartCustomer_id = %s
                ''', (customer_id,))

                kpis = cur.fetchone()

                total_sales = kpis[0] if kpis[0] is not None else 0
                total_discount = kpis[1] if kpis[1] is not None else 0
                total_vat = kpis[2] if kpis[2] is not None else 0

                print(customer_id, customer_name)
                print(f"Total Sales: {total_sales}")
                print(f"Total Discount: {total_discount}")
                print(f"Total VAT: {total_vat}")

                return render_template('manager_dashboard.html', custo_id=customer_id, custo_name=customer_name,
                                       sales=total_sales, discount=total_discount, vat=total_vat)
            else:
                flash('Customer not found.', 'danger')
                return redirect(url_for('mainmenu.mainmenu'))
        else:
            flash('You need to log in first.', 'danger')
            return redirect(url_for('store_manager.login_manager'))

    except Exception as e:
        logger.error(f'Error during fetching manager data: {e}')
        flash('An error occurred. Please select function from main menu.', 'danger')
        return redirect(url_for("mainmenu.mainmenu"))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

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
    if 'manager_id' in session:
        session.pop('manager_id', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('mainmenu.mainmenu'))
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

