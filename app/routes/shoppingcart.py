
# Includes db access functions:
# add_product_to_cart, update_product_quantity, delete_product_from_cart, finalize_purchase, cart_contents

from flask import Flask, request, jsonify, session, Blueprint, request, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from __init__ import db, logger

shoppingcart_bp = Blueprint('shoppingcart', __name__)

@shoppingcart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    cart_id = data['cart_id']
    product_id = data['product_id']
    quantity = data['quantity']
    add_product_to_cart(cart_id, product_id, quantity)
    return jsonify({'message': 'Product added to cart'})

@shoppingcart_bp.route('/update-cart', methods=['POST'])
def update_cart():
    data = request.json
    cart_id = data['cart_id']
    product_id = data['product_id']
    quantity = data['quantity']
    update_product_quantity(cart_id, product_id, quantity)
    return jsonify({'message': 'Cart updated'})

@shoppingcart_bp.route('/delete-from-cart', methods=['POST'])
def delete_from_cart():
    data = request.json
    cart_id = data['cart_id']
    product_id = data['product_id']
    delete_product_from_cart(cart_id, product_id)
    return jsonify({'message': 'Product deleted from cart'})

@shoppingcart_bp.route('/finalize-purchase', methods=['POST'])
def finalize_purchase_route():
    data = request.json
    cart_id = data['cart_id']
    finalize_purchase(cart_id)
    return jsonify({'message': 'Purchase finalized'})

@shoppingcart_bp.route('/cart-contents', methods=['GET'])
def cart_contents():

    customer_id = session.get('customer_id')
    if 'customer_id' in session:
        logger.debug(f"Customer ID {customer_id} in current session.")
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

    cartcustomer_id = int(customer_id)
    print(f"cartcustomer_id: {cartcustomer_id}")

    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cart_contents = []  # Initialize cart_contents to avoid UnboundLocalError

    try:
        cur.execute(
            '''SELECT
            scp.cart_id,
            scp.product_id,
            scp.quantity,
            p.id,
            p.productName,
            p.productDetails,
            p.productSalesPrice,
            p.productDiscount,
            (p.productSalesPrice * scp.quantity) AS total_price,
            (p.productDiscount * scp.quantity) AS total_discount,
            ((p.productSalesPrice * scp.quantity) * 0.25) AS total_vat -- Assuming 25% VAT
            FROM
                MStore_v1.ShoppingCart sc,
                MStore_v1.ShoppingCartProduct scp
            JOIN
                MStore_v1.Product p ON scp.product_id = p.id
            WHERE
                scp.cart_id = 3
                AND
                sc.cartcustomer_id = cartcustomer_id
                AND
                sc.cartStatus = FALSE
                ;''')

        cart_contents = cur.fetchall()

        # Convert Decimal to float
        cart_contents = [
            (
                item[0], item[1], item[2], item[3], item[4], item[5],
                float(item[6]), float(item[7]), float(item[8]), float(item[9]), float(item[10])
            ) for item in cart_contents
        ]

        print(f"Query results: {cart_contents}")  # Debugging line

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return render_template('shoppingcart_contents.html', cart_contents=cart_contents)


# DB access functions

def add_product_to_cart(cart_id, product_id, quantity):

    # Connect to the database
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    logger.debug('db connected')

    cur.execute( """INSERT INTO ShoppingCartProduct(cart_id, product_id, quantity) VALUES (%s, %s, %s) ON CONFLICT (cart_id, product_id) DO UPDATE SET quantity = ShoppingCartProduct.quantity + EXCLUDED.quantity""", (cart_id, product_id, quantity))

    conn.commit()
    cur.close()
    conn.close()

    flash('Product added to cart successfully!', 'success')
    logger.debug('Product added to cart successfully!')

def update_product_quantity(cart_id, product_id, quantity):

    # Connect to the database
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    logger.debug('db connected')

    cur.execute("""UPDATE ShoppingCartProduct SET quantity = %s WHERE cart_id = %s AND product_id = %s""",
    (quantity, cart_id, product_id))

    conn.commit()
    cur.close()
    conn.close()

    flash('Product updated to cart successfully!', 'success')
    logger.debug('Product updated to cart successfully!')

def delete_product_from_cart(cart_id, product_id):

    # Connect to the database
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    logger.debug('db connected')

    cur.execute(
        """
        DELETE FROM ShoppingCartProduct
        WHERE cart_id = %s AND product_id = %s
        """, (cart_id, product_id))

    conn.commit()
    cur.close()
    conn.close()

    flash('Product deleted from cart successfully!', 'success')
    logger.debug('Product deleted from cart successfully!')


def finalize_purchase(cart_id):

    # Connect to the database
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    logger.debug('db connected')

    cur.execute(
        """
        UPDATE ShoppingCart
        SET cartStatus = TRUE, cartPurchasedTime = NOW()
        WHERE id = %s
        """, (cart_id,))

    conn.commit()
    cur.close()
    conn.close()

    flash('Cart purchase finalized successfully!', 'success')
    logger.debug('Cart purchase finalized successfully!')
