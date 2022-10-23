from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'



from app import routes, models, errors
from app.models import User,Admin




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    u = Admin.query.filter_by(email="nuwayuwa@gmail.com")
    if u is None:
        superadmin = Admin(email="nuwayuwa@gmail.com")
        superadmin.set_password('nuway123')
        db.session.add(superadmin)
        db.session.commit()

    return app