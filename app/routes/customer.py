from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_session import Session
import psycopg2
import bcrypt
import re # regular expressions
import bleach # sanitization
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from __init__ import db, logger

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
                    return redirect(url_for('customer.customer_dashboard'))

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


@customer_bp.route('/customer/view_cart/<int:cart_id>')
def view_cart(cart_id):
    # Fetch the shopping cart details from the database using cart_id
    cart = get_cart_by_id(cart_id)  # Replace with your actual database query
    print()
    print(cart)
    print()
    return render_template('customer_shopping_carts.html')

def get_cart_by_id(cart_id):
    #return shoppingcart.get_cart_contents(cart_id)
    #Example function to fetch cart details from the database
    return { 'id': cart_id,
        'items': [
            {'product_id': 1, 'product_name': 'Product 1', 'quantity': 2, 'price': 10.0},
            {'product_id': 2, 'product_name': 'Product 2', 'quantity': 1, 'price': 20.0},
        ],
        'total_price': 40.0,
        'total_discount': 5.0,
        'total_vat': 3.0
    }

@customer_bp.route("/shoppingcarts")
def shoppingcarts():
    try:
        if 'customer_id' in session:
            customer_id = session['customer_id']
            conn = db.engine.raw_connection()
            cur = conn.cursor()

            cur.execute("""
                SELECT * FROM mstore_v1.ShoppingCart WHERE cartCustomer_id = %s""", (customer_id,))
            customerCarts = cur.fetchall()

            if customerCarts:
                 cur.close()
                 conn.close()
                 return render_template('customer_shopping_carts.html', shopping_carts=customerCarts)
            else:
                 flash('No shoppincarts found.', 'danger')
                 return redirect(url_for('customer.customer_dashboard'))

        else:
            logger.error(f'Error during fetching customer data: {e}')
            flash('Customer session not found. Please select new function from main menu.', 'danger')
            cur.close()
            conn.close()
            return redirect(url_for('customer_mainmenu.customer_mainmenu'))

    except Exception as e:
        logger.error(f'Error during fetching customer data: {e}')
        flash('An error occurred. Please select function from main menu.', 'danger')
        cur.close()
        conn.close()

    finally:
        cur.close()
        conn.close()
        render_template('customer_dashboard.html')
    return redirect(url_for('customer_mainmenu.customer_mainmenu'))

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
    if 'customer_id' in session:
        session.pop('customer_id', None)
        flash('You have been logged out.', 'success')
        return redirect(url_for('customer_mainmenu.customer_mainmenu'))
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

@customer_bp.route('/customer_dashboard')
def customer_dashboard():
    if 'customer_id' in session:
        customer_id = session.get('customer_id')

        sales = 0.0
        discount = 0.0
        vat = 0.0

    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

    conn = db.engine.raw_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM mstore_v1.customer WHERE id = %s", (customer_id,))

        customer = cur.fetchone()

        if customer:
            customer_id = customer[0]
            customer_name = customer[2]

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

            # Fetch the results
            kpis = cur.fetchone()

            # Extract the KPIs
            total_sales = kpis[0] if kpis[0] is not None else 0
            total_discount = kpis[1] if kpis[1] is not None else 0
            total_vat = kpis[2] if kpis[2] is not None else 0

            # Print or use the KPIs as needed (for testing)
            print(customer_id)
            print(f"Total Sales: {total_sales}")
            print(f"Total Discount: {total_discount}")
            print(f"Total VAT: {total_vat}")
            return render_template('customer_dashboard.html', custo_id=customer_id, custo_name=customer_name, sales=total_sales, discount=total_discount, vat=total_vat)
        else:
            logger.error(f'Error during fetching customer data: {e}')
            flash('Customer data not found. Please select function.', 'danger')
            redirect(url_for("customer_mainmenu.customer_mainmenu"))

    except Exception as e:
        logger.error(f'Error during fetching customer data: {e}')
        flash('An error occurred. Please select function from main menu.', 'danger')
        return redirect(url_for("customer_mainmenu.customer_mainmenu"))

    finally:
        if cur:
           cur.close()
        if conn:
           conn.close()

    return redirect(url_for("customer_mainmenu.customer_mainmenu"))