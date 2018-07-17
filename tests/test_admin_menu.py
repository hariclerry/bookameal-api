import unittest
import pytest
from bookameal import app
from flask import json,jsonify
from flask_jwt_extended import create_access_token

import os
from bookameal.config import app_config
from bookameal.models import User, Meal, Menu, Order
from bookameal.application import app, db

from create_admin import create_admin


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

        create_admin()

        login_admin = json.dumps({
            "email":"admin@bookameal.com","password":"12345",})

        response = self.tester.post('/api/v1/auth/login',content_type="application/json",data=login_admin)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        db.drop_all()


    def test_create_menu(self):
        meal1 = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal1,headers=self.headers)

        meal2 = json.dumps(
            {"meal_option": "beans and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal2,headers=self.headers)


        menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
        self.assertIn("Menu has been created",rv.data.decode())

    def test_create_menu_code(self):
        menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
        self.assertEqual(rv.status_code,422)


    def test_get_menu(self):
        # the meal option "tomatoes and rice" comes from the meals created in the 'test_meals.py' file
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        # these two tests are similar, but implemented in a diffrent fashion
        assert b"[]" in rv.data
        self.assertIn("[]", rv.data.decode())

    def test_get_menu_code(self):
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    def test_you_cant_create_similar_menu_twice(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)

        menu = json.dumps({"date":"2018-09-07","menu":[1]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        self.assertIn("The date you provided already has a menu",rv.data.decode())


    def test_create_menu_with_non_exixting_meal(self):
        menu = json.dumps({"date":"2018-09-07","menu":[1]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        self.assertIn("You provided a meal id that does not exist",rv.data.decode())

    def test_create_menu_with_wrong_date_format(self):
        menu = json.dumps({"date":"2018-09-7","menu":[1]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        self.assertIn("Wrong date format provided!, The format is Year-Month-Day(eg, 2018-01-01)",rv.data.decode())
















