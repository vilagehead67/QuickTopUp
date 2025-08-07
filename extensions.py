# extensions.py
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_mail import Mail

mongo = PyMongo()
bcrypt = Bcrypt()
mail = Mail()


