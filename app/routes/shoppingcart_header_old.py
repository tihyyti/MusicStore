from flask import Flask, request, jsonify, Blueprint, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from __init__ import db, logger

shoppingcart_header_bp = Blueprint('shoppingcart_header', __name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(dbname="mstore_v1", user="your_user", password="your_password", host="your_host")
    return conn

# List all carts
@shoppingcart_header_bp.route('/list-carts', methods=['GET'])
def list_carts():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM mstore_v1.shoppingcart")
    carts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('list_carts.html', carts=carts)

# Create a new cart
@shoppingcart_header_bp.route('/create-cart', methods=['POST'])
def create_cart():
    data = request.form
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
    return redirect(url_for('shoppingcart_header.list_carts'))

# Delete a cart
@shoppingcart_header_bp.route('/delete-cart/<int:cart_id>', methods=['POST'])
def delete_cart(cart_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mstore_v1.shoppingcart WHERE id = %s", (cart_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Cart deleted successfully!', 'success')
    return redirect(url_for('shoppingcart_header.list_carts'))

# Get cart contents
@shoppingcart_header_bp.route('/cart-contents/<int:cart_id>', methods=['GET'])
def cart_contents(cart_id):
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
    cur.close()
    conn.close()
    return render_template('cart_contents.html', contents=contents)
