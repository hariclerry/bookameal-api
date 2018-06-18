from flask import jsonify
from .models import User, MealOption, Menu, Order


class Validator:

    def __init__(self, data={}):
        self.data = data

    def signup(self):
        if self.data['password'] != self.data['password_conf']:
            return "passwordError"
        elif "@" not in self.data['email'] or "." not in self.data['email']:
            return "emailError"
        elif len(self.data['name']) < 1 or len(self.data['email']) < 1 or len(self.data['location']) < 1 or len(self.data['password']) < 1 or len(self.data['password_conf']) < 1:
            return "missingDataError"
        elif User.check_if_email_exists(self.data['email']):
            return "emailExists"
        else:
            return True

    def signup_message(self):
        if self.signup() == "passwordError":
            return jsonify({"message": "Passwords don't match!"}), 422
        elif self.signup() == "emailError":
            return jsonify({"message": "Wrong email format!"}), 422
        elif self.signup() == "missingDataError":
            return jsonify({"message": "Some required data missing!"}), 422
        elif self.signup() == "userExists":
            return jsonify({"message":"The email address given already exists!"}), 422
        else:
            return True

    def create_meal(self):
        if len(self.data['meal_option']) < 1:
            return "meal_optionError"
        elif not isinstance(self.data['meal_option_price'], int):
            return "meal_option_priceError"
        else:
            return True

    def create_meal_message(self):
        if self.create_meal() == "meal_optionError":
            return jsonify({"message": "No meal option provided!"}), 422
        elif self.create_meal() == "meal_option_priceError":
            return jsonify({"message": "The price provided has an error!"}), 422

    def edit_meal_message(self):
        if self.create_meal() == "meal_optionError":
            return jsonify({"message": "No meal option provided!"}), 422
        elif self.create_meal() == "meal_option_priceError":
            return jsonify({"message": "The price provided has an error!"}), 422

    def create_menu(self):
        if len(self.data['date']) < 8:
            return "dateError"
        elif len(self.data['menu']) < 1:
            return "menuError"
        else:
            return True

    def create_menu_message(self):
        if self.create_menu() == "dateError":
            return jsonify({"message": "The date provided is wrong or is in a wrong format!, The format is Year-Month-Day"}), 422
        elif self.create_menu() == "menuError":
            return jsonify({"message": "Atleast one meal is required for the menu!"}), 422

    def create_order(self):
        if not isinstance(self.data['customer_id'], int):
            return "customer_idError"
        elif len(self.data['date']) < 8:
            return "dateError"
        elif not isinstance(self.data['meal_option_id'],int):
            return "meal_option_idError"
        else:
            return True

    def create_order_message(self):
        if self.create_order() == "customer_idError":
            return jsonify({"message": "Your session must have expired! Login and try again"}), 422
        elif self.create_order() == "dateError":
            return jsonify({"message": "The date provided is wrong or is in a wrong format!, The format is Year-Month-Day"}), 422
        elif self.create_order() == "meal_option_idError":
            return jsonify({"message": "No valid meal id provided"}), 422
