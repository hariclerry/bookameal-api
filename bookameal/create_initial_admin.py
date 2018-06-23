# This file is only for creating the first bookameal admin when
# the application starts, the admin may later login and create other admins

from .models import User

admin = User()
data={
    "name":"admin",
    "email":"admin@bookameal.com",
    "password":"12345",
    "password_conf":"12345",
    "isAdmin":True,
    "location":"Kampala"
}

admin.save(data)