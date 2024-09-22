from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
#Create the database tables before the first request

def create_tables():
    db.create_all()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)

    bcrypt = Bcrypt(app)

    # Custom filter to format datetime
    def format_datetime(value, format="%Y-%m-%d %H:%M:%S"):
        if value is None:
            return ""
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime(format)

    # Register the custom filter
    app.jinja_env.filters['datetime'] = format_datetime
    print("Custom datetime filter registered")

    with app.app_context():

        create_tables()

        # Import and register blueprints
        from routes.home import home_bp
        from routes.custoregist import custoregist_bp
        #from routes.prodgroup import prodgroup_bp
        # from routes.product import product_bp
        # from routes.shoppingcart import shoppingcart_bp
        # from routes.productimage import productimage_bp
        # from routes.store import store_bp
        # from routes.reg_customer import reg_customer_bp
        from routes.store_manager import store_manager_bp
        from routes.customer_dashboard_old import customer_dashboard_bp
        from routes.customer_dashboard import customer_dashboard_bp




        # Register blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(custoregist_bp)
        # app.register_blueprint(prodgroup_bp)
        # app.register_blueprint(product_bp)
        # app.register_blueprint(shoppingcart_bp)
        # app.register_blueprint(productimage_bp)
        # app.register_blueprint(store_bp)
        # app.register_blueprint(reg_customer_bp)
        app.register_blueprint(store_manager_bp)
        app.register_blueprint(customer_dashboard_bp)

    return app