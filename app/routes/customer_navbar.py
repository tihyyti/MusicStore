from flask import Blueprint, render_template, flash
#from flask_session import Session
from __init__ import db, logger
import templates

customer_navbar_bp = Blueprint('customer_navbar', __name__)

@customer_navbar_bp.route('/customer_navbar')
def customer_navbar():

    #flash('Select a function from the navigation menu.', 'success')
    return render_template('customer_navbar.html')
