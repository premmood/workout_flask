from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    # Force Jinja to auto-reload templates
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    #sqlalchemy related
    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    # Optional: make sure debug is on (helps reload)
    app.debug = True

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)
    #On every request, it calls your load_user() function with that ID.
    '''This line works only if your User class inherits from UserMixin, because it gives Flask-Login the methods it 
    needs (is_authenticated, get_id(), etc.).'''
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    return app


