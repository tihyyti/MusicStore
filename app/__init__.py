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
    def format_datetime(value, format="%Y-%m-%d %H:%M"):
        if value is None:
            return ""
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime(format)

    # Register the custom filter
    app.jinja_env.filters['datetime'] = format_datetime
    print("Custom datetime filter registered")

    with app.app_context():

        #create_tables()

        # Import and register blueprints
        from routes.home import home_bp
        from routes.mainmenu import mainmenu_bp
        from routes.register_customer import customerregist_bp
        from routes.register_manager import managerregist_bp
        from routes.store_manager import store_manager_bp
        from routes.login_customer import login_customer_bp
        from routes.customer_dashboard import customer_dashboard_bp
        # from routes.prodgroup import prodgroup_bp
        # from routes.product import product_bp
        # from routes.shoppingcarts import shoppingcarts_bp
        from routes.shoppingcart import shoppingcart_bp
        #from .customer import customer_bp

        # from routes.productimage import productimage_bp
        # from routes.store import store_bp

        # Register blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(mainmenu_bp)
        app.register_blueprint(customerregist_bp)
        app.register_blueprint(login_customer_bp)
        app.register_blueprint(managerregist_bp)
        app.register_blueprint(store_manager_bp)
        app.register_blueprint(customer_dashboard_bp)
        # app.register_blueprint(prodgroup_bp)
        # app.register_blueprint(product_bp)
        #app.register_blueprint(shoppingcarts_bp)
        app.register_blueprint(shoppingcart_bp, url_prefix='/shoppingcart')
        #app.register_blueprint(customer_bp, url_prefix='/customer')
        # app.register_blueprint(productimage_bp)
        # app.register_blueprint(store_bp)

    return app