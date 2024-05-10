from random import random, randint
from typing import Sequence

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProductDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    relationShip = db.relationship('Product', backref='categories', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    imageName = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    employee = db.relationship('Employee', backref='orders')
    products = db.relationship('Product', secondary='order_product', backref='orders')


order_product = db.Table(
    'order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)


@app.route('/api/getProducts', methods=['GET'])
def get_products(product_name):  # put application's code here
    print()


@app.route('/')
def create():
    # category1 = Categories(id=1, name="Корпусы")
    # db.session.add(category1)
    # category2 = Categories(id=2, name="Процессоры")
    # db.session.add(category2)
    # category3 = Categories(id=3, name="Видеокарты")
    # db.session.add(category3)
    # category4 = Categories(id=4, name="ОЗУ")
    # db.session.add(category4)
    # category5 = Categories(id=5, name="Материнские платы")
    # db.session.add(category5)
    # category6 = Categories(id=6, name="SSD")
    # db.session.add(category6)
    # category7 = Categories(id=7, name="Блоки питания")
    # db.session.add(category7)
    # db.session.commit()
    # for i in range(50):
    #     name = "Процессор " + str(i)
    #     price = randint(400, 1500)
    #     description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore"
    #     categoryId = 2
    #     product = Product(name=name, price=price, imageName="CpuImage", description=description, categoryId=categoryId)
    #     db.session.add(product)
    #     db.session.commit()
    # db.session.query(Product).delete()
    # db.session.commit()
    products = Product.query.all()
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'imageName': product.imageName,
            'description': product.description,
            'categoryId': product.categoryId
        })

    return jsonify(data)


if __name__ == '__main__':
    app.run()
