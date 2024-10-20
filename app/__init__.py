import os
from flask import Flask, session, redirect, url_for, flash
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import logging
from datetime import datetime

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

# Create the database tables before the first request
def create_tables():
    db.create_all()
    return

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Custom filter to format datetime
    def format_datetime(value, format="%Y-%m-%d %H:%M"):
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime(format)
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime(format)

    with app.app_context():
        create_tables()

        # Import and register blueprints
        from routes.home import home_bp
        from routes.mainmenu import mainmenu_bp
        from routes.manager_navbar import manager_navbar_bp
        from routes.customer_mainmenu import customer_mainmenu_bp
        from routes.customer_navbar import customer_navbar_bp
        from routes.register_customer import customerregist_bp
        from routes.register_manager import managerregist_bp
        from routes.customer import customer_bp
        from routes.store_manager import store_manager_bp
        from routes.shoppingcart_header import shoppingcart_header_bp
        from routes.shoppingcart import shoppingcart_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(mainmenu_bp)
        app.register_blueprint(manager_navbar_bp)
        app.register_blueprint(customer_mainmenu_bp)
        app.register_blueprint(customer_navbar_bp)
        app.register_blueprint(customerregist_bp)
        app.register_blueprint(managerregist_bp)
        app.register_blueprint(customer_bp, url_prefix='/customer')
        app.register_blueprint(store_manager_bp, url_prefix='/manager')
        app.register_blueprint(shoppingcart_header_bp, url_prefix='/cart')
        app.register_blueprint(shoppingcart_bp, url_prefix='/shoppingcart')

        app.jinja_env.filters['datetime'] = format_datetime
        print("Custom datetime filter registered")

    return app

def check_manager_logged_in():
    manager_id = session.get('manager_id')
    if manager_id:
        logger.debug(f"Manager ID {manager_id} in current session.")
        return int(manager_id)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_manager'))

def check_customer_logged_in():
    customer_id = session.get('customer_id')
    if customer_id:
        logger.debug(f"Customer ID {customer_id} in current session.")
        return int(customer_id)
    else:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('store_manager.login_customer'))
