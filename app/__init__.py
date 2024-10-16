import os
from flask import Flask
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()

# Create the database tables before the first request
def create_tables():
    db.create_all()
    return

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt = Bcrypt(app)
    csrf = CSRFProtect(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Custom filter to format datetime
    def format_datetime(value, format="%Y-%m-%d %H:%M"):
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime(format)
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime(format)

    # Register the custom filter
    app.jinja_env.filters['datetime'] = format_datetime
    print("Custom datetime filter registered")

    with app.app_context():
        create_tables()

        # Import and register blueprints
        from routes.home import home_bp
        from routes.mainmenu import mainmenu_bp
        from routes.customer_mainmenu import customer_mainmenu_bp
        from routes.register_customer import customerregist_bp
        from routes.register_manager import managerregist_bp
        from routes.customer import customer_bp
        from routes.store_manager import store_manager_bp
        from routes.shoppingcart_header import shoppingcart_header_bp
        from routes.shoppingcart import shoppingcart_bp
        # from routes.prodgroup import prodgroup_bp
        # from routes.product import product_bp
        # from routes.productimage import productimage_bp
        # from routes.store import store_bp

        # Register blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(mainmenu_bp)
        app.register_blueprint(customer_mainmenu_bp)
        app.register_blueprint(customerregist_bp)
        app.register_blueprint(managerregist_bp)
        app.register_blueprint(customer_bp, url_prefix='/customer')
        app.register_blueprint(store_manager_bp, url_prefix='/manager')
        app.register_blueprint(shoppingcart_header_bp, url_prefix='/cart')
        app.register_blueprint(shoppingcart_bp, url_prefix='/shoppingcart')
        # app.register_blueprint(prodgroup_bp)
        # app.register_blueprint(product_bp)
        # app.register_blueprint(productimage_bp)
        # app.register_blueprint(store_bp)

    return app
