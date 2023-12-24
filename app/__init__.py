from flask import Flask
# from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from urllib.parse import quote
from os import environ
from flask_bootstrap import Bootstrap
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

# Load environment variables from .env file (only during development)
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL', f'mysql://root:{quote("P@ssw0rd1234567")}@localhost/flask_template')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Initialize bcrypt
# bcrypt = bcrypt(app)

# Bootstrap-Flask requires this line
bootstrap = Bootstrap(app)

# Flask-WTF requires this line
csrf = CSRFProtect(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Register the blueprint
from app.auth.views import auth_views
from app.main.views import main_views
from app.dashboard.views import dashboard_views
app.register_blueprint(auth_views)
app.register_blueprint(main_views)
app.register_blueprint(dashboard_views)


# Initialize Flask-Admin
# admin = Admin(app, name='My Admin', template_mode='bootstrap4')# base_template='admin.html')

###############################################

        
        
from app.auth.views import *
from app.auth.helpers import load_user,unauthorized_callback
