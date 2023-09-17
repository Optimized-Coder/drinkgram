import os
from flask import Flask, request

from .extensions import db, migrate
from .models import User, Photo, followers, Like, Comment

from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    # configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI='sqlite:///db.sqlite3'
    )

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .routes import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    return app