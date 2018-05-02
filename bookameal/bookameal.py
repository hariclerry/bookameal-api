import os
from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify, json, make_response
from .models import User, MealOption, Menu, Order

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .config import app_config

app = Flask(__name__)

app.config.from_object(app_config[
    os.getenv("APP_ENV") or "development"
])

jwt = JWTManager(app)


@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        assert request.method == method


@app.route('/')
def welcome():
    return redirect(url_for('login'))

# register a user


@app.route('/api/v1/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return 'Method not yet impelemented'
    else:
        data = request.get_json()
        User().save(data)
        if data['password'] != data['password_conf']:
            return jsonify({"message": "Passwords don't match!"}), 422
        else:
            access_token = create_access_token(identity=data['email'])
            return jsonify(access_token=access_token), 200


@app.route('/api/v1/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify(User().get_user_info(session['email']))
    else:
        data = request.get_json()
        email = data['email']
        password = data['password']
        if (User().login(email, password)):
            session['email'] = email
            access_token = create_access_token(identity=email)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid login credentials"}), 401


@app.route('/api/v1/home')
def home():
    days = Menu().menus
    return jsonify(days)


@app.route('/api/v1/auth/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


# get all meal options (admin only)
@app.route('/api/v1/meals/', methods=['GET', 'POST'])
# @jwt_required
def manage_meals():
    if request.method == 'GET':
        meal_options = MealOption().json_all()
        return jsonify(meal_options)
    else:
        data = request.get_json()
        MealOption().save(data)
        return jsonify(MealOption().json_all())


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['POST', 'PUT', 'DELETE'])
# @jwt_required
def meal_update(mealid):
    if request.method == 'PUT':
        data = request.get_json()
        MealOption().find(mealid).update(data)
        return jsonify(MealOption().json_all())
    else:
        MealOption().find(mealid).delete()
        return jsonify(MealOption().json_all())


# setup the menu for the day & get the menu for the day (admin only[POST])
@app.route('/api/v1/menu', methods=['GET', 'POST'])
def days_menu():
    if request.method == 'GET':
        return jsonify(Menu().json_all())
    else:
        menu = request.get_json()
        Menu().save(menu)
        return jsonify(Menu().json_all())


# select the meal option from the menu & get all orders (admin only)
@app.route('/api/v1/orders', methods=['GET', 'POST'])
def view_orders():
    if request.method == 'GET':
        return jsonify(Order().json_all())
    else:
        data = request.get_json()
        Order().save(data)
        return jsonify(Order().json_all())


# modify an order
@app.route('/api/v1/orders/<int:orderid>', methods=['POST', 'PUT'])
def order_modify(orderid):
    data = request.get_json()
    Order().find(orderid).update(data)
    return jsonify(Order().json_all())

    date = data['date']
    meal_option = data['meal_option']
    user = User().get_user_info(session.get('email'))
    customer_id = User().users.index(user)

    Order().edit_order(orderid, customer_id, date, meal_option)
    return jsonify(Order().orders)


# Routes that will be used for rendering templates later (These are custom routes)
# Not used in the API
@app.route('/api/v1/my_orders', methods=['GET'])
def my_orders():
    user_email = session.get('email')
    user = User().get_user_info(user_email)
    user_id = User().users.index(user)
    orders = User().my_orders(user_id)
    return render_template('user/my_orders.html', orders=orders)


@app.route('/api/v1/order_details/<int:orderid>', methods=['GET'])
def order_details(orderid):
    order = Order().get_order(orderid)
    user_id = Order().get_order(orderid)['customer_id']
    user = User().get_user_details(user_id)
    return render_template('admin/days_order_details.html', user=user, order=order)

# display the page for setting up a days menu


@app.route('/api/v1/set_menu', methods=['GET'])
def set_menu():
    meals = MealOption().get_all()
    return render_template('admin/set_days_menu.html', meal_options=meals)


# route for getting the menus registered for a day
@app.route('/api/v1/days/<string:day>', methods=['GET'])
def get_days_menu(day):
    menu = Menu().get_a_days_menu(day)
    return jsonify(menu)
