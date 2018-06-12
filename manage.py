from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookameal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db',MigrateCommand)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(35),unique=True)
    origin = db.Column(db.String(25))
    password = db.Column(db.String)

class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer,primary_key=True)
    meal_option = db.Column(db.String(30))
    meal_option_price = db.Column(db.Integer)

class Menu(db.Model):
    __tablename__ = "menus"
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String)
    menu = db.Column(db.Text)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    date = db.Column(db.String)
    meal_option_id = db.Column(db.Integer,db.ForeignKey('meals.id'))

if __name__ == '__main__':
    manager.run()
