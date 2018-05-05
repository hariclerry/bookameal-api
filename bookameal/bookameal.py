import os
from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify, json, make_response
from .models import User, MealOption, Menu, Order

from flasgger import Swagger, swag_from


from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .config import app_config

app = Flask(__name__)

app.config.from_object(app_config[
    os.getenv("APP_ENV") or "development"
])
swagger = Swagger(app)
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


@app.route('/api/v1/auth/signup', methods=['POST'])
@swag_from('/bookameal/docs/signup.yml')
def signup():
    data = request.get_json()
    if data != None:
        User().save(data)
        if data['password'] != data['password_conf']:
            return jsonify({"message": "Passwords don't match!"}), 422
        else:
            message = "welcome, thanks for signing up"
            access_token = create_access_token(identity=data['email'])
            return jsonify(access_token=access_token, message=message), 201


@app.route('/api/v1/auth/login', methods=['POST'])
@swag_from('/bookameal/docs/login.yml')
def login():
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
@app.route('/api/v1/meals/', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_meals.yml')
def create_meals():
    data = request.get_json()
    MealOption().save(data)
    return jsonify(MealOption().json_all()), 201


@app.route('/api/v1/meals/', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_meals.yml')
def get_meals():
    meal_options = MealOption().json_all()
    return jsonify(meal_options), 200


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['PUT'])
@jwt_required
@swag_from('/bookameal/docs/edit_meals.yml')
def meal_update(mealid):
    data = request.get_json()
    MealOption().find(mealid).update(data)
    return jsonify(MealOption().json_all()), 201


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['DELETE'])
@jwt_required
@swag_from('/bookameal/docs/delete_meals.yml')
def meal_delete(mealid):
    MealOption().find(mealid).delete()
    return jsonify({"message": "Meal deleted sucessfully"}), 200


# setup the menu for the day & get the menu for the day (admin only[POST])
@app.route('/api/v1/menu', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_menu.yml')
def get_days_menu():
    return jsonify(Menu().json_all()), 200

# setup the menu for the day & get the menu for the day (admin only[POST])


@app.route('/api/v1/menu', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_menu.yml')
def create_days_menu():
    menu = request.get_json()
    Menu().save(menu)
    return jsonify({"message": "Menu has been created"}), 201


# select the meal option from the menu & get all orders (admin only)
@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_orders.yml')
def view_orders():
    return jsonify(Order().json_all())


@app.route('/api/v1/orders', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_order.yml')
def create_orders():
    data = request.get_json()
    Order().save(data)
    return jsonify({"message": "Order has been created"}), 201


# modify an order
@app.route('/api/v1/orders/<int:orderid>', methods=['POST', 'PUT'])
@swag_from('/bookameal/docs/edit_order.yml')
def order_modify(orderid):
    data = request.get_json()
    Order().find(orderid).update(data)
    return jsonify(Order().json_all()), 201


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
def get_a_days_menu(day):
    menu = Menu().get_a_days_menu(day)
    return jsonify(menu)
