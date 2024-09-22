from flask import Blueprint, render_template, session, redirect, url_for, flash
import psycopg2

customer_dashboard_bp = Blueprint('customer_dashboard', __name__)

@customer_dashboard_bp.route('/customer_shopping_carts')
def customer_shopping_carts():
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            customer_id,
            customer_name,
            cart_id,
            cart_status,
            edited_time,
            purchased_time,
            delivery_time,
            cart_category
        FROM CustomerShoppingCarts
        ORDER BY cart_category DESC, edited_time DESC, purchased_time DESC, delivery_time DESC
    """)
    shopping_carts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('customer_shopping_carts.html', shopping_carts=shopping_carts)
