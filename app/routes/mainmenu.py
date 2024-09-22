from flask import Blueprint, render_template

mainmenu_bp = Blueprint('mainmenu', __name__)

@mainmenu_bp.route('/')
def mainmenu():
    return render_template('mainmenu.html')