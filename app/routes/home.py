from flask import Blueprint, render_template
import templates

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    return render_template('mainmenu.mainmenu.html')

if __name__ == "__main__":
    app.run(debug=True)
