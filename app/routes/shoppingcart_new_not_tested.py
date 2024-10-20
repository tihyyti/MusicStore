from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from __init__ import db, logger, csrf
from wtforms import Form, IntegerField, validators
from routes.shoppingcart_header import shoppingcart_header_list

shoppingcart_bp = Blueprint('shoppingcart', __name__)

class CartForm(Form):
    cart_id = IntegerField('Cart ID', [validators.DataRequired()])
    product_id = IntegerField('Product ID', [validators.DataRequired()])
    quantity = IntegerField('Quantity', [validators.DataRequired(), validators.NumberRange(min=1)])

@shoppingcart_bp.route('/add-to-cart', methods=['PUT'])
@csrf.exempt
def add_to_cart():
    form = CartForm(request.form)
    if form.validate():
        cart_id = form.cart_id.data
        product_id = form.product_id.data
        quantity = form.quantity.data
        add_product_to_cart(cart_id, product_id, quantity)
        return jsonify({'message': 'Product added to cart'})
    else:
        return jsonify({'message': 'Invalid input'}), 400

@shoppingcart_bp.route('/update-cart', methods=['POST'])
@csrf.exempt
def update_cart():
    form = CartForm(request.form)
    if form.validate():
        cart_id = form.cart_id.data
        product_id = form.product_id.data
        quantity = form.quantity.data
        update_product_quantity(cart_id, product_id, quantity)
        return jsonify({'message': 'Cart updated'})
    else:
        return jsonify({'message': 'Invalid input'}), 400

@shoppingcart_bp.route('/delete-from-cart', methods=['POST'])
@csrf.exempt
def delete_from_cart():
    form = CartForm(request.form)
    if form.validate():
        cart_id = form.cart_id.data
        product_id = form.product_id.data
        delete_product_from_cart(cart_id, product_id)
        return jsonify({'message': 'Product deleted from cart'})
    else:
        return jsonify({'message': 'Invalid input'}), 400

@shoppingcart_bp.route('/finalize-purchase', methods=['POST'])
@csrf.exempt
def finalize_purchase_route():
    form = CartForm(request.form)
    if form.validate():
        cart_id = form.cart_id.data
        finalize_purchase(cart_id)
        return jsonify({'message': 'Purchase finalized'})
    else:
        return jsonify({'message': 'Invalid input'}), 400


@shoppingcart_bp.route('/cart-contents', methods=['GET'])
def cart_contents():
    if 'customer_id' not in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('customer.login_customer'))

    customer_id = session['customer_id']
    logger.debug(f"Customer ID {customer_id} in current session.")
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cart_contents = []

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
            ((p.productSalesPrice * scp.quantity) * 0.25) AS total_vat
            FROM
                MStore_v1.ShoppingCart sc,
                MStore_v1.ShoppingCartProduct scp
            JOIN
                MStore_v1.Product p ON scp.product_id = p.id
            WHERE
                scp.cart_id = 3
                AND
                sc.cartcustomer_id = %s
                AND
                sc.cartStatus = FALSE
                ;''', (customer_id,))

        cart_contents = cur.fetchall()

        cart_contents = [
            (
                item[0], item[1], item[2], item[3], item[4], item[5],
                float(item[6]), float(item[7]), float(item[8]), float(item[9]), float(item[10])
            ) for item in cart_contents
        ]

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return render_template('shoppingcart_list.html', carts=cart_contents)
