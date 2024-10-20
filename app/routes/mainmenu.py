from flask import Blueprint, render_template, flash
import templates

mainmenu_bp = Blueprint('mainmenu', __name__)

@mainmenu_bp.route('/')
def mainmenu():
    #flash('Select a function from the navigation menu.', 'success')
    return render_template('main_menu.html')

