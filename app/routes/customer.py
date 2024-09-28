from flask import Flask, Blueprint, request, render_template, redirect, url_for, flash, session
import psycopg2
import bcrypt
from datetime import datetime
from __init__ import db, logger

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    if request.method == 'POST':
        custoName = request.form['custoName']
        custoPassw = request.form['custoPassw']

        conn = db.engine.raw_connection()
        cur = conn.cursor()
        logger.debug('db connected')

        try:
            cur.execute("SELECT id, custoPassw FROM mstore_v1.Customer WHERE custoName = %s", (custoName,))
            customer = cur.fetchone()

            if customer is not None:
                if custoPassw and bcrypt.checkpw(custoPassw.encode('utf-8'), customer[1].encode('utf-8')):
                    cur.execute("UPDATE mstore_v1.Customer SET last_login = %s WHERE id = %s", (datetime.now(), customer[0]))
                    conn.commit()
                    flash('Login successful!', 'success')
                    cur.close()
                    conn.close()
                    return redirect(url_for('mainmenu.mainmenu'))
                else:
                    flash('Invalid username or password.', 'danger')
                    logger.error('customer not found')
            else:
                flash('No customer record in the system !.', 'danger')
                logger.error('Customer not found')

        except Exception as e:
            logger.error(f'Error during login: {e}')
            flash('An error occurred. Please try again.', 'danger')

        finally:
            cur.close()
            conn.close()

    return render_template('login_customer.html')

@customer_bp.route("/report/<report_name>")
def report(report_name):
    if 'customer_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM {report_name}"
        cur.execute(query)
        report_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('report.html', report_name=report_name,
report_data=report_data)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

@customer_bp.route('/basic_listing/<listing_name>')
def basic_listing(listing_name):
    if 'customer_id' in session:
        conn = db.engine.raw_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM {listing_name}"
        cur.execute(query)
        listing_data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('basic_listing.html', listing_name=listing_name,
listing_data=listing_data)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

@customer_bp.route('/logout_customer')
def logout_customer():
    session.pop('manager_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('customer.login_customer'))

customer_dashboard_bp = Blueprint('customer_dashboard', __name__)

@customer_bp.route('/customer_dashboard')
def customer_dashboard():

    sales = 0.0
    discount = 0.0
    vat = 0.0

    customer_id = 1  # Replace with actual customer ID from session or login
    if not 'customer' in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

    conn = db.engine.raw_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM mstore_v1.ShoppingCart WHERE cartCustomer_id = %s', (customer(id)))
    order_history = cur.fetchall()

    # Fetch KPIs per customer
    for shoppingcart in order_history:

        cur.execute('SELECT cartvat,  cartdiscount, carttotal FROM mstore_v1.ShoppingCart WHERE cartCustomer_id = %s',(cartcustomer_id,))
        shoppingcart = cur.fetchone()

        sales = sales + shoppingcart.carttotal
        discount = discount + shoppingcart.cartdiscount
        vat = vat + shoppingcart.cartvat

    cur.close()
    conn.close()

    print(sales)
    print(discount)
    print(vat)
    return render_template('customer_dashboard.html', sales=sales, discount=discount, vat=vat)