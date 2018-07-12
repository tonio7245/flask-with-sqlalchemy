from flask import Flask
from config import Config
from dotenv import load_dotenv
 # Order is important here!

try:
    load_dotenv()
except:
    pass # Heroku does not use .env


app = Flask(__name__)
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)
db = SQLAlchemy(app)

from models import Product
from schemas import products_schema



@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/')
def hello():
    return "Hello World!"
