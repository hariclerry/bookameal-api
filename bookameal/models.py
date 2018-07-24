from sqlalchemy import Column, String, Integer, Boolean
# from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash
from .application import app, db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    location = Column(String)
    password = Column(String)
    isAdmin = Column(Boolean, default=False, nullable=False)
    orders = db.relationship("Order", backref="user")

    def __init__(
            self,
            name=None,
            email=None,
            location=None,
            password=None,
            isAdmin=False):
        self.name = name
        self.email = email
        self.location = location
        self.password = password
        self.isAdmin = isAdmin

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    @staticmethod
    def check_if_email_exists(email):

        user = User.query.filter_by(email=email).first()
        if user is not None:
            return "emailUsed"
        return user

    @staticmethod
    def is_admin(email):
        user = User.query.filter_by(email=email).first()

        if user.isAdmin:
            return True
        return False

    def before_save(self):
        user = User().where("email", self.email)

        if user != []:
            return False
        else:
            return True

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if not user:
            return False

        if check_password_hash(user.password, password):
            return True
        return False


datemenu = db.Table(
    "datemenu",
    db.Column(
        "meal_id",
        db.Integer,
        db.ForeignKey("meals.id")),
    db.Column(
        "menu_id",
        db.Integer,
        db.ForeignKey("menus.id")))


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    meal_option = db.Column(db.String(30), unique=True)
    meal_option_price = db.Column(db.Integer)
    orders = db.relationship("Order", backref="meal")

    def __init__(self, meal_option=None, meal_option_price=None):
        self.meal_option = meal_option
        self.meal_option_price = meal_option_price

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    def update(self, id, data):
        meal = Meal.query.filter_by(id=id).first()
        meal.meal_option = data['meal_option']
        meal.meal_option_price = data['meal_option_price']
        db.session.commit()

    def delete(self, mealid):
        meal = Meal.query.filter_by(id=mealid).first()
        db.session.delete(meal)
        db.session.commit()

    @staticmethod
    def get_all():
        meals = []
        for meal in Meal().query.all():
            meal = {
                'id': meal.id,
                'meal_option': meal.meal_option,
                'meal_price': meal.meal_option_price
            }
            meals.append(meal)
        return meals

    def check_meal_existence(self, meal_option):
        clean_meal = meal_option.lower().strip()
        meal_option = Meal.query.filter_by(meal_option=clean_meal).first()
        if meal_option is not None:
            return "mealRegistered"
        return "mealNotRegistered"

    def check_meal_ids(self, ids):
        for id in ids:
            meal = Meal.query.filter_by(id=id).first()
            if not meal:
                return "unfoundId"
        return "allMealsExist"


class Menu(db.Model):

    __tablename__ = "menus"
    # __table_args__ = (
    #     db.UniqueConstraint('date', 'name', name='unix_menu'),
    # )
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    category = db.Column(db.String(100), default="lunch")
    # orders = db.relationship("Order",backref="name")
    meals = db.relationship(
        "Meal",
        secondary=datemenu,
        backref=db.backref(
            "menus",
            lazy="dynamic"))

    def __init__(self, date=None, meal_ids=None, category=None):
        self.date = date
        self.category = category
        self.menu = meal_ids

    def save(self):
        menu = Menu.query.filter_by(
            date=self.date,
            category=self.category).first() or False
        if menu:
            return False
        db.session.add(self)
        for id in self.menu:
            meal = Meal.query.filter_by(id=id).first()
            self.meals.append(meal)
        db.session.commit()
        db.session.rollback()
        return True


    def check_menu_existence(self, date_id, category=None, mealid=None):
        menu = Menu.query.filter_by(date=date_id, category=category)
        if menu is None:
            return "menuNotRegistered"
        return "menuRegistered"


    def check_for_meal_in_menu(self, mealid, menu_id, category):
        menu = Menu.query.filter_by(date=menu_id, category=category).first()
        print(menu)
        menu_meal_ids = []

        if menu is not None:
            for meal in menu.meals:
                menu_meal_ids.append(meal.id)

            if mealid not in menu_meal_ids:
                return "menuHasNoMeal"
            return "menuHasMeal"
        return "menuHasNoMeal"

    def get_meals(date):
        menu = Menu.query.filter_by(date=date).first()
        return menu.meals

    @staticmethod
    def get_all():
        data = []
        dates = []
        menus = Menu.query.all()
        if not menus:
            return []

        for menu in menus:
            date = menu.date
            if date not in dates:
                dates.append(date)

        for date in dates:
            menus = Menu.query.filter_by(date=date)

            breakfast = []
            lunch = []
            dinner = []
            supper = []
            for menu in menus:

                for meal in menu.meals:
                    meal = {
                        "id": meal.id,
                        "meal_option": meal.meal_option,
                        "meal_option_price": meal.meal_option_price
                    }
                    print('category', menu.category)
                    print('category type', type(menu.category))
                    if menu.category == 'breakfast':
                        breakfast.append(meal)
                    elif menu.category == 'lunch':
                        lunch.append(meal)
                    elif menu.category == 'dinner':
                        dinner.append(meal)
                    elif menu.category == 'supper':
                        supper.append(meal)
            day_menus = {
                "breakfast": breakfast,
                "lunch": lunch,
                "dinner": dinner,
                "supper": supper}
            data.append({"date": date, "menu": day_menus})
        return data


class Order(db.Model):

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey("menus.id"), nullable=False)
    menu_category_id = db.Column(
        db.Integer,
        db.ForeignKey("menus.id"),
        nullable=False)

    meal_option_id = db.Column(
        db.Integer,
        db.ForeignKey('meals.id'),
        nullable=False)

    date = db.relationship("Menu", foreign_keys=[date_id])
    menu_category = db.relationship("Menu", foreign_keys=[menu_category_id])

    def __init__(
            self,
            customer_id=None,
            date_id=None,
            menu_name_id=None,
            meal_option_id=None):
        self.customer_id = customer_id
        self.date_id = date_id
        self.menu_category_id = menu_name_id
        self.meal_option_id = meal_option_id

    def save(self, plates, customer_id, date_id, menu_name_id, meal_option_id):

        for plate in range(0, plates):
            order = Order(customer_id, date_id, menu_name_id, meal_option_id)
            db.session.add(order)
            db.session.commit()
            db.session.rollback()

    def update(self, id, data):
        order = Order.query.filter_by(id=id).first()
        db_id = Menu.query.filter_by(
            date=data['date'],
            category=data['menu_category']).first().id

        order.customer_id = data['customer_id']
        order.date_id = db_id
        order.menu_category_id = db_id
        order.meal_option_id = data['meal_option']
        db.session.commit()

    def get_all(self):
        data = []
        orders = Order.query.all()
        if orders == []:
            return []
        for order in orders:

            order = {
                "id": order.id,
                "customer": order.user.name,
                "meal": order.meal.meal_option,
                "price": order.meal.meal_option_price,
                "date": order.date.date,
                "name": order.date.category
            }
            data.append(order)
        return data
