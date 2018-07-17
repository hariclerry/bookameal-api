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

    def tearDown(self):
        db.drop_all()


    def test_signup_code(self):
    	user = json.dumps(
    		{
    		"name": "Nabaasa Richard", "location": "Kampala",
            "email": "nabaasarichard@gmail.com", "password": "default",
             "password_conf": "default"
    		})
    	rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
    	self.assertEqual(rv.status_code,201)

    def test_signup_message(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasa@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("welcome, thanks for signing up", rv.data.decode())


    def test_signup_token(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasaricharcook@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("access_token", rv.data.decode())

    def test_signup_with_wrong_credentials(self):
            user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                               "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "different"})
            rv = self.app.post('/api/v1/auth/signup',
                               content_type="application/json", data=user)
            self.assertIn("Passwords don't match!", rv.data.decode())

