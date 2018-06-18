from .BaseModel import Model
from flask import abort, Flask
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

from .application import app


# db_string = 'postgresql:///bookameal'

# db_session = scoped_session(sessionmaker(
#     autocommit=False, autoflush=False, bind=db_string))



db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    location = Column(String)
    password = Column(String)

    def __init__(self,name=None,email=None,location=None,password=None):
        self.name = name
        self.email = email
        self.location = location
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    def before_persist(self):
        self.isAdmin = False
        del self.password_conf

    def before_save(self):
        user = User().where("email", self.email)
        if user != []:
            return False
        else:
            return True
    @staticmethod
    def login(email, password):
        # user = db.session.execute("SELECT * FROM users where email = 'email' ")
        user = User.query.filter_by(email=email, password=password).first()        
        if user is  not None:
            return True
        return False

    def my_orders(self, user_id):
        return Order().get_user_orders(user_id)


class MealOption(db.Model):
    __tablename__ = "meal_options"
    id = db.Column(db.Integer,primary_key=True)
    meal_option = db.Column(db.String(30))
    meal_option_price = db.Column(db.Integer)

    def __init__(self,meal_option=None,meal_option_price=None):
        self.meal_option = meal_option
        self.meal_option_price = meal_option_price

    
    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    @staticmethod
    def get_all():
        return MealOption.query.all()



class Menu(db.Model):

    __tablename__ = "menus"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String,unique=True)
    menu = db.Column(db.Text)

    def __init__(self,date=None,menu=None):
        self.date=date
        self.menu=menu

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

    def before_save(self):
        menu = Menu().where("date", self.date)
        if menu != []:
            return False
        else:
            return True



class Order(db.Model):

    __tablename__ = "orders"
    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    date = db.Column(db.String)
    meal_option_id = db.Column(db.Integer,db.ForeignKey('meal_options.id'))

    def __init__(self,customer_id,date,meal_option_id):
        self.customer_id=customer_id
        self.date=date
        self.meal_option_id=meal_option_id

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.rollback()

