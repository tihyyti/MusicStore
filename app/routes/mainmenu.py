from flask import Blueprint, render_template, flash
import templates

mainmenu_bp = Blueprint('mainmenu', __name__)

@mainmenu_bp.route('/')
def mainmenu():
    flash('Select an option from the navigation menu.', 'success')
    return render_template('main_menu.html')

if __name__ == "__main__":
    from my_flask_app import create_app
    app = create_app()
    app.run(debug=True)
