from flask import Flask
from flask_autodoc import Autodoc
from config import Config_Disp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config_Disp)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
bootstrap = Bootstrap(app)
auto = Autodoc(app)
mail = Mail(app)

from app import routes, models, emails
