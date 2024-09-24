from flask import Blueprint, render_template, session, redirect, url_for, flash
import psycopg2
import templates
from routes.login_customer import login_customer
from __init__ import db, logger

customer_dashboard_bp = Blueprint('customer_dashboard', __name__)

@customer_dashboard_bp.route('/dashboard')
def customer_dashboard(customer):

    user_id = 1  # Replace with actual customer ID from session or login

    if not 'customer' in session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('login_customer.login_customer'))

    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM "Customer" WHERE id = %s', (customer(id)))
    customer_details = cur.fetchone()

    cur.execute('SELECT * FROM "ShoppingCart" WHERE cartCustomer_id = %s', (customer(id)))
    order_history = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('customer_dashboard.html', customer_details=customer_details, order_history=order_history)
