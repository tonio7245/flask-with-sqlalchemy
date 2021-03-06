from flask import Flask, request, render_template
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


@app.route('/api/v1/products', methods=['GET'])
def products():
    products = db.session.query(Product).all()
    return products_schema.jsonify(products)

@app.route('/api/v1/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.query(Product).get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return (f"{product.name} was deleted",202)
    else:
        return('already deleted or not existing',202)

@app.route('/api/v1/products', methods=['POST'])
def add_product():
    product = Product()
    product.name = request.form['name']
    db.session.add(product)
    db.session.commit()
    return (product_schema.jsonify(product),201)


@app.route('/api/v1/products/<int:id>', methods=['PATCH'])
def change_product(id):
    product = db.session.query(Product).get(id)
    product.name = request.form['name']
    db.session.commit()
    return (product_schema.jsonify(product),200)


@app.route('/api/v1/products/<int:id>')
def get_product(id):
    product = db.session.query(Product).get(id)
    return product_schema.jsonify(product)


@app.route('/')
def hello():
    products = db.session.query(Product).all()
    return render_template('home.html',products = products)

@app.route('/product/<int:id>')
def display_product(id):
    product = product = db.session.query(Product).get(id)
    return render_template('product.html',product = product)
