from flask import Blueprint, render_template, flash
#from flask_session import Session
from __init__ import db, logger
import templates

customer_mainmenu_bp = Blueprint('customer_mainmenu', __name__)

@customer_mainmenu_bp.route('/customer_mainmenu')
def customer_mainmenu():

    #flash('Select a function from the navigation menu.', 'success')
    return render_template('customer_mainmenu.html')
