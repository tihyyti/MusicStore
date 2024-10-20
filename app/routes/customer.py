from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_session import Session
import psycopg2
import bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from __init__ import db, logger
import routes.shoppingcart as shoppingcart


customer_bp = Blueprint('customer', __name__)

# Validation functions
def validate_name(name):
    return bool(re.match("^[A-Za-z\s]+$", name))
def validate_password(password):
    return len(password) >= 8

@customer_bp.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    if request.method == 'POST':
         # Clean the input using bleach (sanitization)
        custoName = bleach.clean(request.form['custoName'])
        custoPassw = bleach.clean(request.form['custoPassw'])

        # Validate the inputs:
        # Name Validation: Name must contain only letters and spaces.
        is_name_valid = validate_name(custoName)
        # Password Validation: Checks if the password is at least 8 characters long.
        is_password_valid = validate_password(custoPassw)

        # Check all validations
        if is_name_valid and is_password_valid:
            customerStatus = True
        else:
            customerStatus = False

        # Output the validation results for input testing
        print(f"Name valid: {is_name_valid}")
        print(f"Password valid: {is_password_valid}")

        try:
            conn = None
            cur = None
            conn = db.engine.raw_connection()
            cur = conn.cursor()
            logger.debug('db connected')
            cur.execute("SELECT id, custoPassw FROM mstore_v1.customer WHERE custoName = %s",
            (custoName,))

            customer = cur.fetchone() # tuple of the customer’s ID and the stored password

            if customer:
                customer_id, stored_passw = customer # tuple unpacking
                if customerStatus and custoPassw and bcrypt.checkpw(custoPassw.encode('utf-8'), stored_passw.encode  ('utf-8')):
                    cur.execute("UPDATE mstore_v1.customer SET last_login = %s WHERE id = %s", (datetime.now(), customer_id))
                    conn.commit()
                    session['customer_id'] = customer_id
                    logger.debug(f"Customer ID {customer_id} set in session.")
                    flash('Login successful!', 'success')
                    return redirect(url_for('customer_navbar.customer_navbar'))

                else:
                    # Check validations
                    if not is_name_valid and not is_password_valid:
                        flash('Invalid username and password.', 'danger')
                    elif not is_name_valid:
                        flash('Invalid username.', 'danger')
                    else:
                        flash('Invalid password.', 'danger')

                    logger.error('customer not found, wrong credentials.')
            else:
                flash('No customer record in the system !.', 'danger')
                logger.error('Customer not found, wrong credentials.')

        except Exception as e:
            logger.error(f'Error during login: {e}')
            flash('An error occurred. Please try again.', 'danger')

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template('login_customer.html')


@customer_bp.route('/view-cart')
def view_cart():

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
        logger.debug(f"customer ID {customer_id} in current session.")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

    # Fetch the shopping cart item details
    cartcustomer_id = int(customer_id)
    shoppingcarts = []
    shoppingcarts = shoppingcart.cart_contents()
    print()
    print(f"view_cart/Fetched shopping carts: {shoppingcart}")
    print()

    conn = None
    cur = None
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    logger.debug('db connected')

    cur.execute("SELECT * FROM mstore_v1.customer WHERE id = %s", (cartcustomer_id,))

    customer = cur.fetchone()
    if customer:
        customer_id = int(customer[0])
        customer_name = customer[2]
        customer_email = customer[3]
        print(f"Customer ID: {customer_id}, Name: {customer_name}, email: {customer_email}")
        # Fetch item sums per shoppingcart
        cur.execute('''
            SELECT
                carttotal AS total_sales,
                cartdiscount AS total_discount,
                cartvat AS total_vat
            FROM mstore_v1.Shoppingcart
            WHERE cartcustomer_id = %s
        ''', (cartcustomer_id,))

        # Fetch cartcustomer cart totals
        cart_totals = cur.fetchone()
        # Extract the cart_totals
        total_sales = cart_totals[0] if cart_totals[0] is not None else 0
        total_discount = cart_totals[1] if cart_totals[1] is not None else 0
        total_vat = cart_totals[2] if cart_totals[2] is not None else 0

        # Print or use the cart_totals as needed (for testing)
        print(f"Total Sales: {total_sales}")
        print(f"Total Discount: {total_discount}")
        print(f"Total VAT: {total_vat}")

        return render_template('customer_dashboard.html', custo_id=customer_id,
        custo_name=customer_name, custo_email=customer_email, sales=total_sales,
        discount=total_discount, vat=total_vat)
    else:
        logger.error(f'Error during fetching customer data: {e}')
        flash('Customer data not found. Please select function.', 'danger')
        redirect(url_for("customer_navbar.customer_navbar"))

    return render_template('customer_shopping_carts.html', shopping_carts=shoppingcarts)

@customer_bp.route("/shoppingcarts")
def list_shoppingcarts():
    try:
        customer_id = session.get('customer_id')
        if 'customer_id' in session:
            logger.debug(f"customer ID {customer_id} in current session.")
        else:
            flash('You need to log in first.', 'danger')
            return redirect(url_for('customer.login_customer'))

        cartcustomer_id = int(customer_id)
        conn = db.engine.raw_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT * FROM mstore_v1.Shoppingcart WHERE cartcustomer_id = %s""", (cartcustomer_id,))

        customerCarts = cur.fetchall()

        if customerCarts:
            return render_template('customer_shopping_carts.html', shopping_carts=customerCarts)
        else:
            flash('No shoppincarts found.', 'danger')
            return redirect(url_for('customer_navbar.customer_navbar'))

    except Exception as e:
        logger.error(f'Error during fetching customer data: {e}')
        flash('An error occurred. Please select function from main menu.', 'danger')

    finally:

        if cur:
            cur.close()
        if conn:
            conn.close()

    return redirect(url_for('customer_navbar.customer_navbar'))

@customer_bp.route('/customer_dashboard')
def customer_dashboard():

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
       logger.debug(f"customer ID {customer_id} in current session.")
    else:
       flash('You need to log in first.', 'danger')
       return redirect(url_for('customer.login_customer'))

    customer_id = int(customer_id)
    sales = 0.0
    discount = 0.0
    vat = 0.0

    conn = db.engine.raw_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM mstore_v1.customer WHERE id = %s", (customer_id,))

        customer = cur.fetchone()

        if customer:
            customer_id = int(customer[0])
            customer_name = customer[2]
            customer_email = customer[3]

            print(f"Customer ID: {customer_id}, Name: {customer_name}, email: {customer_email}")

            # Fetch aggregated KPIs per customer
            cur.execute('''
                SELECT
                    SUM(carttotal) AS total_sales,
                    SUM(cartdiscount) AS total_discount,
                    SUM(cartvat) AS total_vat
                FROM mstore_v1.ShoppingCart
                WHERE cartCustomer_id = %s
            ''', (customer_id,))

            # Fetch the results
            kpis = cur.fetchone()

            # Extract the KPIs
            total_sales = kpis[0] if kpis[0] is not None else 0
            total_discount = kpis[1] if kpis[1] is not None else 0
            total_vat = kpis[2] if kpis[2] is not None else 0

            # Print or use the KPIs as needed (for testing)
            print(f"Total Sales: {total_sales}")
            print(f"Total Discount: {total_discount}")
            print(f"Total VAT: {total_vat}")
            return render_template('customer_dashboard.html', custo_id=customer_id, custo_name=customer_name, custo_email=customer_email, sales=total_sales, discount=total_discount, vat=total_vat)
        else:
            logger.error(f'Error during fetching customer data: {e}')
            flash('Customer data not found. Please select function.', 'danger')
            redirect(url_for("customer_mainmenu.customer_mainmenu"))

    except Exception as e:
        logger.error(f'Error during fetching customer data: {e}')
        flash('An error occurred. Please select function from customer main menu.', 'danger')
        return redirect(url_for("customer_mainmenu.customer_mainmenu"))

    finally:
        if cur:
           cur.close()
        if conn:
           conn.close()

    return redirect(url_for("shoppingcart_header.shoppingcart_header_list"))

@customer_bp.route('/logout_customer')
def logout_customer():
    if 'customer_id' in session:
        session.pop('customer_id', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('mainmenu.mainmenu'))
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))
