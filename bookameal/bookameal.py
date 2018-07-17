from flask import request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify, json, make_response

from werkzeug.security import generate_password_hash

from .models import User, Meal, Menu, Order
from .Validator import Validator

from flasgger import Swagger, swag_from

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .application import app

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
    if Validator(data).signup() != True:
        return Validator(data).signup_message()
    else:
        hashed_pw = generate_password_hash(data['password'])
        User(data['name'],data['email'],data['location'],hashed_pw).save()
        session['email'] = data['email']
        message = "welcome, thanks for signing up"
        access_token = create_access_token(identity=data['email'])
        return jsonify(access_token=access_token, message=message), 201


@app.route('/api/v1/auth/login', methods=['POST'])
@swag_from('/bookameal/docs/login.yml')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if User.login(email, password):
        session['email'] = email
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid login credentials"}), 401


@app.route('/api/v1/auth/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))


# get all meal options (admin only)
@app.route('/api/v1/meals/', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_meals.yml')
def create_meals():
    if User.is_admin(session['email']):
        data = request.get_json()
        if Validator(data).create_meal() != True:
            return Validator(data).create_meal_message()
        else:
            Meal(data['meal_option'],data['meal_option_price']).save()
            return jsonify({"message":"Meal created successfully"}), 201
    return jsonify({"message":"Only an admin can create a meal"}), 401


@app.route('/api/v1/meals/', methods=['GET'])
@swag_from('/bookameal/docs/get_meals.yml')
@jwt_required
def get_meals():
    if User.is_admin((session['email'])):
        return jsonify(Meal.get_all()), 200
    return jsonify({"message":"Only an admin can view meals"}), 401


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['PUT'])
@jwt_required
@swag_from('/bookameal/docs/edit_meals.yml')
def meal_update(mealid):
    if User.is_admin((session['email'])):
        data = request.get_json()
        if Validator(data).create_meal() != True:
            return Validator(data).edit_meal_message()
        else:
            Meal().update(mealid, data)
            return jsonify({"message":"Meal updated successfully"}), 200
    return jsonify({"message":"Only an admin can edit meals"}), 401

# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['DELETE'])
@jwt_required
@swag_from('/bookameal/docs/delete_meals.yml')
def meal_delete(mealid):
    if User.is_admin((session['email'])):
        Meal().delete(mealid)
        return jsonify({"message": "Meal deleted sucessfully"}), 200
    return jsonify({"message":"Only an admin can delete a meal"}), 401

# setup the menu for the day & get the menu for the day (admin only[POST])
@app.route('/api/v1/menu', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_menu.yml')
def get_days_menu():
    return jsonify(Menu.get_all())


# setup the menu for the day & get the menu for the day (admin only[POST])


@app.route('/api/v1/menu', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_menu.yml')
def create_days_menu():
    if User.is_admin(session['email']):
        data = request.get_json()
        if Validator(data).create_menu() != True:
            return Validator(data).create_menu_message()
        else:
            Menu(data['date'],data['menu']).save()
            return jsonify({"message": "Menu has been created"}), 201
    return jsonify({"message": "Only admin can create a menu"}), 401


# select the meal option from the menu & get all orders (admin only)
@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_orders.yml')
def view_orders():
    if User.is_admin(session['email']):
        return jsonify(Order().get_all())
    return jsonify({"message":"Only an admin can view orders"}), 401


@app.route('/api/v1/orders', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_order.yml')
def create_orders():
    data = request.get_json()
    if Validator(data).create_order() != True:
        return Validator(data).create_order_message()
    else:
        Order(data['customer_id'],data['date'],data['meal_option']).save()
        return jsonify({"message": "Order has been created"}), 201


# modify an order
@app.route('/api/v1/orders/<int:orderid>', methods=['POST', 'PUT'])
@jwt_required
@swag_from('/bookameal/docs/edit_order.yml')
def order_modify(orderid):
    data = request.get_json()
    if Validator(data).create_order() != True:
        return Validator(data).create_order_message()
    else:
        Order().update(orderid, data)
        return jsonify({"message": "Order has been edited"}), 201


@app.route('/api/v1/auth/create_admin',methods=['POST'])
@jwt_required

def create_admin():
    if User.is_admin(session['email']):
        data = request.get_json()
        if Validator(data).signup() != True:
            return Validator(data).signup_message()
        else:
            hashed_pw = generate_password_hash(data['password'])
            User(data['name'],data['email'],data['location'],hashed_pw,data['is_admin']).save()
            message = "Admin registered"
            return jsonify(message=message), 201
    return jsonify({"message":"Only an admin can register another admin"})
    









