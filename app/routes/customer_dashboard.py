from flask import Blueprint, render_template, session, redirect, url_for, flash
import psycopg2

customer_dashboard_bp = Blueprint('customer_dashboard', __name__)

@customer_dashboard_bp.route('/custodashboard')
def custodashboard():
    customer_id = 1  # Replace with actual customer ID from session or login
    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "Customer" WHERE id = %s', (customer_id,))
    customer_details = cur.fetchone()
    cur.execute('SELECT * FROM "ShoppingCart" WHERE cartCustomer_id = %s', (customer_id,))
    order_history = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('custodashboard.html', customer_details=customer_details, order_history=order_history)
