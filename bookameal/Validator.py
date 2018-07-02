from flask import jsonify
from .models import User,MealOption,Menu,Order
import re


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
        elif User().check_email_existence(self.data['email']) == "emailUsed":
            return "duplicateEmailError"
        else:
            return True

    def signup_message(self):
        if self.signup() == "passwordError":
            return jsonify({"message": "Passwords don't match!"}), 422
        elif self.signup() == "emailError":
            return jsonify({"message": "Wrong email format!"}), 422
        elif self.signup() == "missingDataError":
            return jsonify({"message": "Some required data missing!"}), 422
        elif self.signup() == "duplicateEmailError":
            return jsonify({"message":"Email already used!"}), 422
        else:
            return True

    def create_meal(self):
        if len(self.data['meal_option']) < 1:
            return "meal_optionError"
        elif not isinstance(self.data['meal_option_price'], int):
            return "meal_option_priceError"
        elif MealOption().check_meal_existence(self.data['meal_option']) == "mealRegistered":
            return "duplicateMealError"
        else:
            return True

    def create_meal_message(self):
        if self.create_meal() == "meal_optionError":
            return jsonify({"message": "No meal option provided!"}), 422
        elif self.create_meal() == "meal_option_priceError":
            return jsonify({"message": "The price provided has an error!"}), 422
        elif self.create_meal() == "duplicateMealError":
            return jsonify({"message":"The meal has already been registered"}), 422

    def edit_meal_message(self):
        if self.create_meal() == "meal_optionError":
            return jsonify({"message": "No meal option provided!"}), 422
        elif self.create_meal() == "meal_option_priceError":
            return jsonify({"message": "The price provided has an error!"}), 422

    def create_menu(self):
        if len(self.data['menu']) < 1:
            return "menuError"
        elif Menu().check_menu_existence(self.data['date']) == "menuRegistered":
            return "duplicateMenuError"
        elif MealOption().check_meal_ids(self.data['menu']) == "unfoundId":
            return "mealIdError"
        else:
            return True

    def create_menu_message(self):
        if not self.date(self.data['date']):
            return jsonify({"message": "Wrong date format provided!, The format is Year-Month-Day(eg, 2018-01-01)"}), 422
        elif self.create_menu() == "menuError":
            return jsonify({"message": "Atleast one meal is required for the menu!"}), 422
        elif self.create_menu() == "duplicateMenuError":
            return jsonify({"message":"The date you provided already has a menu"}), 422
        elif self.create_menu() == "mealIdError":
            return jsonify({"message":"You provided a meal id that does not exist"}), 422

    def create_order(self):
        if not isinstance(self.data['customer_id'], int):
            return "customer_idError"
        elif not isinstance(self.data['meal_option'],int):
            return "meal_optionError"
        elif Menu().check_menu_existence(self.data['date']) == "menuNotRegistered":
            return "menuNotRegisteredError"
        elif Menu().check_for_meal_in_menu(self.data['meal_option'],self.data['date']) == "menuHasNoMeal":
            return "noMealInMenuError"
        else:
            return True

    def create_order_message(self):
        if self.create_order() == "customer_idError":
            return jsonify({"message": "Your session must have expired! Login and try again"}), 422
        elif not self.date(self.data['date']):
            return jsonify({"message": "Wrong date format provided!, The format is Year-Month-Day(eg, 2018-01-01)"}), 422
        elif self.create_order() == "meal_optionError":
            return jsonify({"message": "Provide a valid meal id"}), 422
        elif self.create_order() == "menuNotRegisteredError":
            return jsonify({"message":self.data['date']+" has no menu registered"}), 422
        elif self.create_order() == "noMealInMenuError":
            return jsonify({"message":"The meal provided is not in the menu for "+self.data['date']}), 422

    def date(self,date):
            date_pattern =  r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
            result = re.match(date_pattern,date)
            if result:
                return True
            return False




