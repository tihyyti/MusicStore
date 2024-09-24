from flask import Blueprint, render_template
import templates

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    from my_flask_app import create_app
    app = create_app()
    app.run(debug=True)
