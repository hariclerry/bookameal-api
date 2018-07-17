import unittest
import pytest
from bookameal import app
from flask import json,jsonify
from flask_jwt_extended import create_access_token

import os
from bookameal.config import app_config
from bookameal.models import User, Meal, Menu, Order
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

        sign_up_user = json.dumps({
            "name":"richard","email":"admin@bookameal.com","password":"12345",
            "password_conf":"12345","location":"Kampala"
            })
        response = self.tester.post('/api/v1/auth/signup',content_type="application/json",data=sign_up_user)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        db.drop_all()


    def test_create_menu(self):
    	menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
    	rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
    	self.assertIn("Only admin can create a menu",rv.data.decode())

    def test_create_menu_code(self):
    	menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
    	rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)


    def test_get_menu(self):
    	# the meal option "tomatoes and rice" comes from the meals created in the 'test_meals.py' file
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        # these two tests are similar, but implemented in a diffrent fashion
        assert b"[]" in rv.data
        self.assertIn("[]", rv.data.decode())

    def test_get_menu_code(self):
        menu = json.dumps(
            {"date": "2018-09-07", "menu": ["fish and matooke", "milk and bread"]})

        self.tester.post('/api/v1/menu',
                      content_type="application/json", data=menu,headers=self.headers)
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        self.assertTrue(rv.status_code, 200)







