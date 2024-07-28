#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = '1807d9a2a3568d294a578a5379a650b7'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from app.menu_routes import menu_bp
app.register_blueprint(menu_bp)

# Import blueprints and register them
from app.orders_routes import orders_bp
app.register_blueprint(orders_bp, url_prefix='/orders')


# Import routes after registering blueprints
from app import routes
