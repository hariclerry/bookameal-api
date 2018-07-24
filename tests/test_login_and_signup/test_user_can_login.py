import unittest
import pytest
from bookameal import app
from flask import json

import os
from bookameal.config import app_config
from bookameal.models import User, Meal, Menu, Order
from bookameal.application import app, db


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(app_config[os.getenv("APP_ENV") or "testing"])
        db.create_all()
        self.app = app.test_client()
        self.login_url = '/api/v1/auth/login'

    def tearDown(self):
        db.drop_all()

    # Test user cannot login with wrong credentials
    def test_login_with_wrong_credentials(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post(self.login_url,
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 401)
        self.assertIn("Invalid login credentials", rv.data.decode())

    # Test user can login
    def test_login_successfully(self):
        signup_user = json.dumps({
            "name":"richard",
            "email":"richard@bookameal.com",
            "password":"12345",
            "password_conf":"12345",
            "location":"Kampala"
            })

        self.app.post("api/v1/auth/signup",data=signup_user,content_type="application/json")

        user = json.dumps(
            {"email": "richard@bookameal.com", "password": "12345"})
        rv = self.app.post(self.login_url,
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 200)

