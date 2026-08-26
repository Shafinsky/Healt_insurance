from flask import Flask
from config import Config
from extensions import db, login_manager, migrate, mail
from routes import main_bp

def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False 
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flask_login import current_user

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)
    migrate.init_app(app, db)

    from routes import main_bp
    from auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)