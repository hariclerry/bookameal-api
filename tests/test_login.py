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
        sign_up_user = json.dumps({
            "name":"richard","email":"richard@bookameal.com","password":"12345",
            "password_conf":"12345","location":"Kampala"
            })
        response = self.app.post('/api/v1/auth/signup',content_type="application/json",data=sign_up_user)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        db.drop_all()
        

    def test_login_code(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 401)

    def test_login_code_success(self):
        user = json.dumps(
            {"email":"richard@bookameal.com","password":"12345"})
        rv = self.app.post('/api/v1/auth/login',
                            content_type="application/json",data=user)
        self.assertEqual(rv.status_code,200)

    def test_login_message(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertIn("Invalid login credentials", rv.data.decode())




