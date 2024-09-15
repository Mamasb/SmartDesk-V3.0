from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Ensure you have a proper config class in config.py

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Import here to avoid circular import
        return User.query.get(int(user_id))

    return app
