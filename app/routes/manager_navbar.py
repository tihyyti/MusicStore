from flask import Blueprint, render_template, flash
#from flask_session import Session
from __init__ import db, logger
import templates

manager_navbar_bp = Blueprint('manager_navbar', __name__)

@manager_navbar_bp.route('/manager_navbar')
def manager_navbar():

    #flash('Select a function from the navigation menu.', 'success')
    return render_template('manager_navbar.html')

