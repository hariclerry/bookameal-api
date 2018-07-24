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

        self.app = app.test_client()
        self.signup_url = '/api/v1/auth/signup'

    def tearDown(self):
        db.drop_all()

    # Test user can sign up
    def test_user_can_signup(self):
        user = json.dumps(
            {
                "name": "Nabaasa Richard", "location": "Kampala",
                "email": "nabaasarichard@gmail.com", "password": "default",
                "password_conf": "default"
            })
        rv = self.app.post(self.signup_url,
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 201)


    # Test user cannot sign up with passwords that don't match
    def test_signup_with_mis_matching_passwords(self):
        user = json.dumps({"name": "Nabaasa Richard",
                           "location": "Kampala",
                           "email": "nabaasarichard@gmail.com",
                           "password": "default",
                           "password_conf": "different"})
        rv = self.app.post(self.signup_url,
                           content_type="application/json", data=user)
        self.assertIn("Passwords don't match!", rv.data.decode())


