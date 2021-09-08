from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
db_name = "website.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fnsdjfsdfsd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main.views import views
    from app.auth.views import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_db(app)

    login = LoginManager(app)
    login.login_view = 'auth.login'
    login.init_app(app)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_db(app):
    if not path.exists('website/' + db_name):
        db.create_all(app=app)
