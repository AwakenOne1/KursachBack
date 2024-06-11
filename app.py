from random import random, randint, sample
from typing import Sequence

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://koyeb-adm:MUGok6f2Rezg@ep-steep-sunset-a2a2mckl.eu-central-1.pg.koyeb.app/koyebdb'
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
def get_products():
    try:
        category_id = request.args.get('category_id')
        products = Product.query.filter_by(categoryId=category_id).all()
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
    except Exception as ex:
        print(ex)
    return jsonify(data)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    employee = Employee.query.filter_by(password=password, username=login).first()
    if employee:
        return jsonify({'full_name': employee.full_name, 'id': employee.id})
    else:
        return jsonify({'error': "no such employee"}), 401


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
    # db.session.query(Product).delete()
    # db.session.commit()
    products = Product.query.all()
    data = []
    # for product in products:
    #     data.append({
    #         'id': product.id,
    #         'name': product.name,
    #         'price': product.price,
    #         'imageName': product.imageName,
    #         'description': product.description,
    #         'categoryId': product.categoryId
    #     })
    employee = Employee(id=1, username="AwakenOne1", password="12345678", full_name="Дубовик А.Д.")
    db.session.add(employee)
    db.session.commit()
    emp = Employee.query.all()
    for empl in emp:
        data.append({
            'id': empl.id,
            'login': empl.username,
            'password': empl.password,
            'full_name': empl.full_name
        })
    return jsonify(data)


@app.route('/api/create_order', methods=['GET'])
def create_order():
    user_id = request.args.get('user_id')
    employee = Employee.query.get(user_id)

    if not employee:
        return jsonify({'error': 'User not found'}), 404

    num_products = randint(1, 7)
    products = sample(Product.query.all(), num_products)

    order = Order(employee=employee)
    order.products = products

    db.session.add(order)
    db.session.commit()

    order_data = {
        'order_id': order.id,
        'products': [{'id': p.id, 'name': p.name, 'price': p.price} for p in order.products]
    }

    return jsonify(order_data)


@app.route('/api/order_stats', methods=['GET'])
def get_order_stats():
    total_orders = Order.query.count()
    total_products_ordered = db.session.query(order_product).count()
    avg_products_per_order = total_products_ordered / total_orders if total_orders > 0 else 0

    stats = {
        'total_orders': total_orders,
        'total_products_ordered': total_products_ordered,
        'avg_products_per_order': round(avg_products_per_order, 2)
    }

    return jsonify(stats)


@app.route('/api/top_products', methods=['GET'])
def get_top_products():
    top_products = db.session.query(
        Product.id, Product.name, db.func.count(order_product.c.product_id).label('total_ordered')
    ).join(order_product).group_by(Product.id).order_by(db.desc('total_ordered')).limit(5).all()

    data = [{
        'id': product.id,
        'name': product.name,
        'total_ordered': product.total_ordered
    } for product in top_products]

    return jsonify(data)


@app.route('/api/category_stats', methods=['GET'])
def get_category_stats():
    category_stats = db.session.query(
        Categories.name, db.func.count(Product.id).label('total_products')
    ).join(Product).group_by(Categories.id).all()

    data = [{
        'category': stat.name,
        'total_products': stat.total_products
    } for stat in category_stats]

    return jsonify(data)


@app.route('/api/employee_order_totals', methods=['GET'])
def get_employee_order_totals():
    employee_order_totals = db.session.query(
        Employee.full_name, db.func.sum(Product.price).label('total_ordered')
    ).join(Order).join(order_product).join(Product).group_by(Employee.id).all()

    data = [{
        'employee': total.full_name,
        'total_ordered': total.total_ordered
    } for total in employee_order_totals]

    return jsonify(data)


if __name__ == '__main__':
    app.run()
