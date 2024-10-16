
# Includes db access functions:
# add_product_to_cart, update_product_quantity, delete_product_from_cart, finalize_purchase, get_cart_contents

from flask import Flask, request, jsonify, session, Blueprint, request, render_template, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
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

@shoppingcart_bp.route('/cart-contents/<int:cart_id>', methods=['GET', 'POST'])
def cart_contents(cart_id):
    print(f"shoppingcart.cart_contents: Received cart_id: {cart_id}")
    contents = get_cart_contents(cart_id)
    print(f"Contents: {contents}")
    return jsonify(contents)


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

def get_cart_contents(cart_id):
    print()
    print(f"Received cart_id: {cart_id}")

    # Connect to the database
    conn = db.engine.raw_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    logger.debug('db connected')
    print(f"Executing query with cart_id: {cart_id}")

    cur.execute(
        """
        SELECT
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
            MStore_v1.ShoppingCartProduct scp
        JOIN
            MStore_v1.Product p ON scp.product_id = p.id
        WHERE
            scp.cart_id = %s
        """, (cart_id,)
    )

    contents = cur.fetchall()
    print(f"shoppingcart.get_cart_contents: Query results: {contents}")

    cur.close()
    conn.close()

    if not contents:
        flash('No shopping carts found for this customer!', 'danger')
        logger.error('No shopping carts found for this customer.')
        return render_template("customer_shopping_carts.html")

    #return contents
    return jsonify(contents)
