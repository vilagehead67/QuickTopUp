from flask import Flask
from flask_login import LoginManager
from flask import session
from config import Config
from dotenv import load_dotenv
from extensions import mongo, bcrypt, mail
from datetime import timedelta
from routes.services_routes import services_bp



import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "SECRET_KEY"  #

# Initialize extensions===---
mongo.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import user_loader AFTER mongo is initialized
from models.user_model import load_user
login_manager.user_loader(load_user)

# Register blueprints AFTER login manager setup
from routes.home_routes import home_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.services_routes import services_bp
from routes.admin_routes import admin_bp
from routes.profile_routes import profile_bp




# app.register_blueprint(services_bp, url_prefix='/services')



app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(services_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.errorhandler(404)
def not_found(e):
    return "404 - Page Not Found", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
