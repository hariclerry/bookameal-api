from .BaseModel import Model
from flask import abort
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
db_string = 'postgresql:///bookameal'

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=db_string))
db = create_engine(db_string)
base = declarative_base()

class User(Model):

    def before_persist(self):
        self.isAdmin = False
        del self.password_conf

    def before_save(self):
        user = User().where("email", self.email)
        if user != []:
            return False
        else:
            return True

    def login(self, email, password):
        user = (User().where("email", email)
                and User().where("password", password))
        if (user != []):
            return True
        else:
            return False

    def my_orders(self, user_id):
        return Order().get_user_orders(user_id)


class MealOption(Model):
    def before_save(self):
        meal_option = MealOption().where("meal_option", self.meal_option)
        if meal_option != []:
            return False
        else:
            return True


class Menu(Model):

    def before_save(self):
        menu = Menu().where("date", self.date)
        if menu != []:
            return False
        else:
            return True

    def get_a_days_menu(self, day):
        i = 0
        while (i < len(self.menus)):
            if self.menus[i]['date'] == day:
                return self.menus[i]
            i = i + 1


class Order(Model):

    def get_user_orders(self, user_id):
        for order in self.orders:
            if order['customer_id'] == user_id:
                return order

    def get_order(self, order_id):
        if self.orders[order_id] in self.orders:
            return self.orders[order_id]
        else:
            return "Order not found"
