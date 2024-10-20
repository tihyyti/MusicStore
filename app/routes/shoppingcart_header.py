from flask import Flask, request, session, jsonify, Blueprint, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from .forms import CartForm
from datetime import datetime
from __init__ import db
import logging

shoppingcart_header_bp = Blueprint('shoppingcart_header', __name__)
logger = logging.getLogger(__name__)

# List all carts of a customer
@shoppingcart_header_bp.route('/list-carts', methods=['GET'])
def shoppingcart_header_list():

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
        logger.debug(f"customer ID {customer_id} in current session.")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))
    cartcustomer_id = int(customer_id)
    conn = db.engine.raw_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT id, cartstore_id, cartcustomer_id, cartstatus, cartvat, cartdiscount, carttotal, cartcurrenttime, carteditedtime, cartpurchasedtime, cartdeliverytime FROM mstore_v1.shoppingcart WHERE cartcustomer_id = %s""",(cartcustomer_id,))

    carts = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('shoppingcart_list.html', carts=carts)

# Create a new cart
@shoppingcart_header_bp.route('/create-cart', methods=['GET', 'POST'])
def shoppingcart_header_create():

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
        logger.debug(f"Customer ID {customer_id} in current session.")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))
    cartcustomer_id = customer_id

    form = CartForm()
    if form.validate_on_submit():
        data = form.data
        conn = db.engine.raw_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO mstore_v1.shoppingcart (cartstore_id, cartcustomer_id, cartstatus, cartvat, cartdiscount, carttotal, carteditedtime, cartpurchasedtime, cartdeliverytime) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['cartstore_id'], cartcustomer_id, data['cartstatus'], data['cartvat'], data['cartdiscount'], data['carttotal'], data['carteditedtime'], data['cartpurchasedtime'], data['cartdeliverytime'])
        )
        conn.commit()
        cur.close()
        conn.close()
        flash('Cart created successfully!', 'success')
        return redirect(url_for('shoppingcart_header.shoppingcart_header_list'))
    return render_template('shoppingcart_create.html', form=form)

# Delete a cart
@shoppingcart_header_bp.route('/delete-cart/<int:id>', methods=['POST'])
def shoppingcart_header_delete(id):

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
        logger.debug(f"Cartcustomer ID {cartcustomer_id} in current session.")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))
    cartcustomer_id = int(customer_id)

    conn = db.engine.raw_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM mstore_v1.shoppingcart WHERE cartcustomer_id = %s AND cartpurchasedtime IS NULL", (cartcustomer_id,))
        conn.commit()
        flash('Cart deleted successfully!', 'success')
        logger.debug('Cart deleted successfully!')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for('shoppingcart_header.shoppingcart_header_list'))