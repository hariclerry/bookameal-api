from flask import jsonify
from .models import User, Meal, Menu, Order
import re


class Validator:

    def __init__(self, data={}):
        self.data = data

    def signup(self):
        if self.data['password'] != self.data['password_conf']:
            return jsonify({"message": "Passwords don't match!"}), 422
        elif not self.email(self.data['email']):
            return jsonify({"message": "Wrong email format!"}), 422
        elif not self.data_exists(self.data):
            return jsonify({"message": "Some required data missing!"}), 422
        elif User().check_if_email_exists(self.data['email']) == "emailUsed":
            return jsonify({"message": "Email already used!"}), 422
        else:
            return True

    def create_meal(self):
        if not self.data_exists({"meal_option": self.data['meal_option']}):
            return jsonify({"message": "Missing data required!"}), 422
        elif not isinstance(self.data['meal_option_price'], int):
            return jsonify(
                {"message": "The price provided has an error!"}), 422
        elif Meal().check_meal_existence(self.data['meal_option']) == "mealRegistered":
            return jsonify(
                {"message": "The meal has already been registered"}), 422
        else:
            return True

    def create_menu(self):
        if not self.data_exists({"menu": self.data['menu']}):
            return jsonify(
                {"message": "Atleast one meal is required for the menu!"}), 422
        elif not self.date(self.data['date']):
            return jsonify(
                {"message": "Wrong date format provided!, The format is Year-Month-Day(eg, 2018-01-01)"}), 422
        elif self.data['name'] not in self.available_menus():
            return jsonify(
                {"message": "Unsupported menu category provided"}), 422
        elif Meal().check_meal_ids(self.data['menu']) == "unfoundId":
            return jsonify(
                {"message": "You provided a meal id that does not exist"}), 422
        elif not self.data_exists({"name": self.data['name']}):
            return jsonify(
                {"message": "No menu name with the provided id"}), 422
        else:
            return True

    def create_order(self):
        if not isinstance(self.data['customer_id'], int):
            return jsonify(
                {"message": "Your session must have expired! Login and try again"}), 422
        elif not isinstance(self.data['meal_option'], int):
            return jsonify(
                {"message": "Meal id should be an integer, not string"}), 422
        elif Menu().check_menu_existence(self.data['date'], self.data['menu_category']) == "menuNotRegistered":
            return jsonify({"message": "Date with id " +
                            str(self.data['date']) + " not found"}), 422
        elif Menu().check_for_meal_in_menu(self.data['meal_option'], self.data['date'], self.data['menu_category']) == "menuHasNoMeal":
            return jsonify({"message": "The meal provided is not in the " +
                            str(self.data['menu_category']) +
                            " menu for date " +
                            str(self.data['date'])}), 422
        else:
            return True

    def date(self, date):
        date_pattern = r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
        result = re.match(date_pattern, date)
        if result:
            return True
        return False

    def email(self, email):
        email_format = r'([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})'
        result = re.match(email_format, email)
        if result:
            return True
        return False

    def data_exists(self, data):
        for i in range(len(data)):
            if len(list(data.values())[i]) < 1:
                return False
        return True

    def available_menus(self):
        return ["breakfast", "lunch", "dinner", "supper"]
