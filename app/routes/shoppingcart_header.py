from flask import Flask, request, session, jsonify, Blueprint, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from .forms import CartForm
from datetime import datetime
from __init__ import db
import logging

shoppingcart_header_bp = Blueprint('shoppingcart_header', __name__)
logger = logging.getLogger(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(dbname="MStore_v1", user="postgres", password="postinLent0", host="127.0.0.1")
    return conn

# List all carts of a customer
@shoppingcart_header_bp.route('/list-carts', methods=['GET'])
def shoppingcart_header_list():
    customerid = session.get('customer_id')
    logger.debug(f"Customer ID {customerid} in current session.")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT id, cartstore_id, cartcustomer_id, cartstatus, cartvat, cartdiscount, carttotal, cartcurrenttime,carteditedtime, cartpurchasedtime, cartdeliverytime FROM mstore_v1.shoppingcart WHERE cartcustomer_id = %s""",(customerid,))

    carts = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('shoppingcart_list.html', carts=carts)
    # Alternatively return JSON
    # return jsonify(carts)

# Create a new cart
@shoppingcart_header_bp.route('/create-cart', methods=['GET', 'POST'])
def shoppingcart_header_create():
    cartcustomer_id = session.get('customer_id')
    logger.debug(f"Cartcustomer ID {cartcustomer_id} in current session.")

    form = CartForm()
    if form.validate_on_submit():
        data = form.data
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO mstore_v1.shoppingcart (cartstore_id, cartcustomer_id, cartstatus, cartvat, cartdiscount, carttotal, cartcurrenttime, carteditedtime, cartpurchasedtime, cartdeliverytime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data['cartstore_id'], data['cartcustomer_id'], data['cartstatus'], data['cartvat'], data['cartdiscount'], data['carttotal'], data['cartcurrenttime'], data['carteditedtime'], data['cartpurchasedtime'], data['cartdeliverytime'])
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
    cartcustomer_id = session.get('customer_id')
    logger.debug(f"Cartcustomer ID {cartcustomer_id} in current session.")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mstore_v1.shoppingcart WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Cart deleted successfully!', 'success')
    return redirect(url_for('shoppingcart_header.shoppingcart_header_list'))
#
#Get cart contents
@shoppingcart_header_bp.route('/cart-contents/<int:id>', methods=['GET'])
def shoppingcart_header_contents(id):
    print( "Cart ID=",{id})
    cart_id = id
    cartcustomer_id = session.get('customer_id')
    logger.debug(f"Cartcustomer ID {cartcustomer_id} in current session.")

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        SELECT
            scp.cart_id,
            scp.product_id,
            scp.quantity,
            p.productname,
            p.productdetails,
            p.productsalesprice,
            p.productdiscount,
            (p.productsalesprice * scp.quantity) AS total_price,
            (p.productdiscount * scp.quantity) AS total_discount,
            ((p.productsalesprice * scp.quantity) * 0.25) AS total_vat
        FROM
            mstore_v1.shoppingcartproduct scp
        JOIN
            mstore_v1.product p ON scp.product_id = p.id
        WHERE
            scp.cart_id = %s
        """, (cart_id,)
    )
    contents = cur.fetchall()
    print (contents)

    cur.close()
    conn.close()
    return render_template('shoppingcart_contents.html', id=cart_id)
#