from flask import Flask, request
from config import Config

 # Order is important here!

try:
    from dotenv import load_dotenv
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
from schemas import product_schema


@app.route('/api/v1/products')
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)


@app.route('/api/v1/products', methods=['POST'])
def add_product():
    product = Product()
    product.name = request.form['name']
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/api/v1/products/<int:id>')
def get_product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product)


@app.route('/')
def hello():
    return "Hello World!"
