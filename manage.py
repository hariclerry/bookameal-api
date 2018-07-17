from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from bookameal.application import app, db
from bookameal import models


migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()