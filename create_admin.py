# This file is only for creating the first bookameal admin when
# the application starts, the admin may later login and create other admins

from bookameal.models import User
from werkzeug.security import generate_password_hash
from bookameal.application import app, db
db.create_all()


"""
Creates an admin if there is none
"""

def create_admin():
		admin = User.query.filter_by(isAdmin=True).first()

		if admin:
			print("An admin already exists")
			return

		admin = User()
		admin.name="admin"
		admin.email="admin@bookameal.com"
		admin.password=generate_password_hash("12345")
		admin.isAdmin=True
		admin.location="Kampala"
		admin.save()
		print("Admin created, login with EMAIL:admin@bookameal.com and PASSWORD:12345")

create_admin()

	