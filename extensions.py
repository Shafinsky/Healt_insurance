from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

login_manager.login_view = "auth.login"

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))