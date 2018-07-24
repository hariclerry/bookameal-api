import unittest
import pytest
from bookameal import app
from flask import json, jsonify
from flask_jwt_extended import create_access_token

import os
from bookameal.config import app_config
from bookameal.models import User, Meal, Menu, Order, datemenu
from bookameal.application import app, db


class CheckTestCase(unittest.TestCase):
    def setUp(self):

        app.config.from_object(app_config[os.getenv("APP_ENV") or "testing"])
        db.create_all()
        self.app = app.test_client()

        self.tester = app.test_client()
        app.config['TESTING'] = True
        with self.tester as c:
            with c.session_transaction() as sess:
                sess['email'] = 'admin@bookameal.com'

        sign_up_user = json.dumps({"name": "richard",
                                   "email": "admin@bookameal.com",
                                   "password": "12345",
                                   "password_conf": "12345",
                                   "location": "Kampala"})
        response = self.tester.post(
            '/api/v1/auth/signup',
            content_type="application/json",
            data=sign_up_user)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.url = 'api/v1/menu'

    def tearDown(self):
        db.drop_all()

    # Test normal user not caterer cannot create a menu
    def test_create_menu(self):
        menu = json.dumps({"date": "2018-09-07", "menu": [1, 2]})
        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=menu,
            headers=self.headers)
        self.assertIn("Only admin can create a menu", rv.data.decode())
