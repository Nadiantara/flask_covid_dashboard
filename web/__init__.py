from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#configuration
app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from web import routes