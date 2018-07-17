# This file is only for creating the first bookameal admin when
# the application starts, the admin may later login and create other admins

from bookameal.models import User
from werkzeug.security import generate_password_hash
from bookameal.application import app, db
db.create_all()


def create_admin():
		# Check whether there is an initial admin
		initial = User.query.filter_by(email="admin@bookameal.com").first()
		# Check for any other admin
		other = User.query.filter_by(isAdmin=True).first()
		# Check whether there is any admin in the system
		if bool(initial) or bool(other):
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

	