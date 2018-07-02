import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify, json, make_response
from .models import User, MealOption, Menu, Order
from .Validator import Validator

from flasgger import Swagger, swag_from


from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from .config import app_config

app = Flask(__name__)

app.config.from_object(app_config[
    os.getenv("APP_ENV") or "development"
])
swagger = Swagger(app)
jwt = JWTManager(app)


import bookameal.create_initial_admin


@jwt.expired_token_loader
def my_expired_token_callback():
    return jsonify({
        'msg': 'The token has expired'
    }), 401


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
    data['isAdmin'] = False
    if Validator(data).signup() != True:
        return Validator(data).signup_message()
    else:
        User().save(data)
        message = "welcome, thanks for signing up"
        access_token = create_access_token(identity=data['email'])
        return jsonify({'access_token': access_token, 'message': message}), 201


@app.route('/api/v1/auth/register_admin', methods=['POST'])
@jwt_required
def register_admin():
    data = request.get_json()
    return jsonify(data)


@app.route('/api/v1/auth/login', methods=['POST'])
@swag_from('/bookameal/docs/login.yml')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if (User().login(email, password)):
        session['email'] = email
        access_token = create_access_token(identity=email)
        
        resp = jsonify({"access_token":access_token})
        resp.status_code = 200
        print(resp)
        return resp

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
    data = request.get_json()
    if Validator(data).create_meal() != True:
        return Validator(data).create_meal_message()
    else:
        if User.isAdmin(session['email']):
            MealOption().save(data)
            return jsonify(MealOption().json_all()), 201
        else:
            return jsonify({"message": "Only an admin can create a meal"}), 401


@app.route('/api/v1/meals/', methods=['GET'])
# @jwt_required
@swag_from('/bookameal/docs/get_meals.yml')
def get_meals():
    if User.isAdmin(session['email']):
        meal_options = MealOption().json_all()
        return jsonify(meal_options), 200
    else:
        return jsonify({"message": "Only an admin can view meals in the system"}), 401


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['PUT'])
@jwt_required
@swag_from('/bookameal/docs/edit_meals.yml')
def meal_update(mealid):
    data = request.get_json()
    if Validator(data).create_meal() != True:
        return Validator(data).edit_meal_message()
    else:
        if User.isAdmin(session['email']):
            MealOption().find(mealid).update(data)
            return jsonify(MealOption().json_all()), 201
        else:
            return jsonify({"message": "Only an admin can edit a meal"}), 401


# update information of a meal option (admin only)
@app.route('/api/v1/meals/<int:mealid>', methods=['DELETE'])
@jwt_required
@swag_from('/bookameal/docs/delete_meals.yml')
def meal_delete(mealid):
    if User.isAdmin(session['email']):
        MealOption().find(mealid).delete()
        return jsonify({"message": "Meal deleted sucessfully"}), 200
    else:
        return jsonify({"message": "Only an admin can delete a meal"}), 401


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
    if Validator(menu).create_menu() != True:
        return Validator(menu).create_menu_message()
    else:
        if User.isAdmin(session['email']):
            Menu().save(menu)
            return jsonify({"message": "Menu has been created"}), 201
        else:
            return jsonify({"message": "Only an admin can create a menu"}), 401


# select the meal option from the menu & get all orders (admin only)
@app.route('/api/v1/orders', methods=['GET'])
@jwt_required
@swag_from('/bookameal/docs/get_orders.yml')
def view_orders():
    if User.isAdmin(session['email']):
        return jsonify(Order().json_all())
    else:
        return jsonify({"message": "Only an admin can view orders"}), 401


@app.route('/api/v1/orders', methods=['POST'])
@jwt_required
@swag_from('/bookameal/docs/create_order.yml')
def create_orders():
    data = request.get_json()
    if Validator(data).create_order() != True:
        return Validator(data).create_order_message()
    else:
        Order().save(data)
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
        Order().find(orderid).update(data)
        return jsonify(Order().json_all()), 201


@app.errorhandler(405)
def invalid_method(error):
    return jsonify({"message": "invalid method"}), 405


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "resource not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"message": "something went wrong, try again later"})


# app.config['TRAP_HTTP_EXCEPTIONS'] = True
# @app.errorhandler(Exception)
# def global_handler(e):
#     return jsonify({"message":"Your request could not be processed"}), 500
