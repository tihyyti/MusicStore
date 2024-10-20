from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from __init__ import db, logger, check_manager_logged_in, check_customer_logged_in

store_manager_bp = Blueprint('store_manager', __name__)

# Define functions for each report type
def sales_per_product_group():
    return "Sales per Product Group Report"
def campaign_sales():
    return "Campaign Sales Report"
def sales_per_product():
    return "Sales per Product Report"
def customer_shopping_carts():
    return "Customer Shopping Carts Report"
def customer():
    return "Customer Report"
def productgroup():
    return "Product Group Report"
def product():
    return "Product Report"
def shoppingcart():
    return "Shopping Cart Report"
def store():
    return "Store Report"
def productimage():
    return "Product Image Report"
def shoppingcartproduct():
    return "Shopping Cart Product Report"

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

                    cur.execute(
                        "UPDATE mstore_v1.Store SET last_login = %s WHERE id = %s",
                        (datetime.now(), manager_id),
                    )
                    conn.commit()
                    session['manager_id'] = manager_id
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
            flash('An error occurred. Please select a function from the main menu.', 'danger')
            return redirect(url_for("mainmenu.mainmenu"))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('login_manager.html')

@store_manager_bp.route('/manager_dashboard')
def manager_dashboard():

    manager_id = check_manager_logged_in()
    if isinstance(manager_id, int):

        conn = db.engine.raw_connection()
        cur = conn.cursor()

        try:

            total_sales = 0.0
            total_discount = 0.0
            total_vat = 0.0
            id = 16

            cur.execute("""
                SELECT id, storemanagername, storename, storemanager_id
                FROM mstore_v1.store WHERE id = %s""",(id,))

            store = cur.fetchone()

            if store:
                storemanager_name = store[1]
                store_name = store[2]
                storemanager_id = store[3]
                print(f"ID: {storemanager_id}, Manager: {storemanager_name}, Store: {store_name}")

                return render_template('manager_dashboard.html', manager_id=storemanager_id,    manager_name=storemanager_name, store_name=store_name)
            else:
                flash('Manager account not found.', 'danger')
                return redirect(url_for('mainmenu.mainmenu'))

        except Exception as e:
            logger.error(f'Error during fetching manager-customer data: {e}')
            flash('An error occurred. Please select a function from the main menu.', 'danger')
            return redirect(url_for("mainmenu.mainmenu"))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return redirect(url_for("mainmenu.mainmenu"))

@store_manager_bp.route('/report/<report_name>')
def report(report_name):

        manager_id = check_manager_logged_in()
        if isinstance(manager_id, int):

            # Define case structures
            report = {}
            report = {
                'sales_per_product_group': 'productgroup',
                'campaign_sales': 'product',
                'sales_per_product': 'product'
                }

            # Determine which case structure to use
            handler = report.get(report_name)
            if handler:
                sql_view_name = handler
            else:
                flash('Invalid report name.', 'danger')
                redirect(url_for('mainmenu.mainmenu'))

            conn = db.engine.raw_connection()
            cur = conn.cursor()

            sql_view = f'mstore_v1.{sql_view_name}'
            print({sql_view})

            # Execute a query to get the table column names
            query = f"SELECT * FROM {sql_view} LIMIT 0"
            cur.execute(query)
            column_names = [description[0] for description in cur.description]
            # Print the column names
            print(column_names)

            query = f"SELECT * FROM {sql_view}"
            cur.execute(query)

            report_data = cur.fetchall()

            if cur:
                cur.close()
            if conn:
                conn.close()

            return render_template('report.html', report_name=sql_view_name, report_data=report_data, column_names=column_names)

@store_manager_bp.route('/listing/<listing_name>')
def listing(listing_name):

    manager_id = check_manager_logged_in()
    if isinstance(manager_id, int):

    # Define case structures
        listing = {}
        listing = {
            'shoppingcart': 'shoppingcart',
            'customer': 'customer',
            'productgroup': 'productgroup',
            'product': 'product',
            'store': 'store',
            'productimage': 'productimage',
            'shoppingcartproduct': 'shoppingcartproduct'
        }

        # Determine which case structure to use
        handler = listing.get(listing_name)

        if handler:
            sql_table_name = handler
        else:
            flash('Invalid listing name.', 'danger')
            redirect(url_for('mainmenu.mainmenu'))

        conn = db.engine.raw_connection()
        cur = conn.cursor()

        sql_table = f'mstore_v1.{sql_table_name}'

        # Execute a query to get the table column names
        query = f"SELECT * FROM {sql_table} LIMIT 0"
        cur.execute(query)

        column_names = [description[0] for description in cur.description]
        # Print the column names
        print(column_names)

        query = f"SELECT * FROM {sql_table}"
        cur.execute(query)

        report_data = cur.fetchall()

        if cur:
            cur.close()
        if conn:
            conn.close()

        return render_template('report.html', report_name=sql_table_name, report_data=report_data, column_names=column_names)

@store_manager_bp.route('/logout_manager')
def logout_manager():
    if 'manager_id' in session:
        session.pop('manager_id', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('mainmenu.mainmenu'))
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

