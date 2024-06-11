from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
import json

from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/alexeydubovik/PycharmProjects/Kursach/DB.db'
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

with app.app_context():
    db.create_all()

app.app_context().push()
db.session.commit()


# Функция для загрузки данных из файла JSON в таблицу категорий
def load_categories_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for category in data:
            new_category = Categories(id=category['id'], name=category['name'])
            db.session.add(new_category)
        db.session.commit()


# Функция для загрузки данных из файла JSON в таблицу продуктов
def load_products_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for product in data:
            new_product = Product(
                name=product['name'],
                price=product['price'],
                imageName=product['imageName'],
                description=product['description'],
                categoryId=product['categoryId']
            )
            db.session.add(new_product)
            print("s")
        db.session.commit()


# Путь к файлам JSON
categories_json_file = '/Users/alexeydubovik/categories.json'
products_json_file = '/Users/alexeydubovik/product.json'

# Загрузка данных из файлов JSON в таблицы
with app.app_context():
    load_categories_from_json(categories_json_file)
    load_products_from_json(products_json_file)
