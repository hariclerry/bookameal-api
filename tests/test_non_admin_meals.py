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

    def test_get_meals_code(self):
        meal = {"meal_option": "fish and rice","meal_option_price": 5000}
        self.tester.post('/api/v1/meals/',data=meal,content_type="application/json")
        rv = self.tester.get('/api/v1/meals/',content_type="application/json",headers=self.headers)
        self.assertEqual(rv.status_code, 401)

    def test_get_meals_data(self):
        rv = self.tester.get('/api/v1/meals/')
        self.assertTrue(isinstance(rv.data, object))

    def test_post_meals(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)
        self.assertIn("Only an admin can create a meal", rv.data.decode())


    def test_post_meals_code(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    def test_put_meals(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.tester.put('/api/v1/meals/1',
                          content_type="application/json", data=meal, headers=self.headers)
        self.assertNotIn("Matooke with g-nuts", rv.data.decode())

    def test_put_meals_code(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.tester.put('/api/v1/meals/1',
                          content_type="application/json", data=meal)
        self.assertTrue(rv.status_code, 200)


    def test_delete_meal(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.tester.post('/api/v1/meals/',
                      content_type="application/json", data=meal,headers=self.headers)
        rv = self.tester.delete(
            '/api/v1/meals/1', content_type="application/json")
        self.assertNotIn("Fish", rv.data.decode())

    def test_delete_meal_code(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.tester.post('/api/v1/meals/',
                      content_type="application/json", data=meal,headers=self.headers)
        rv = self.tester.delete(
            '/api/v1/meals/1', content_type="application/json",headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    def test_delete_meal_code(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.tester.post('/api/v1/meals/',
                      content_type="application/json", data=meal,headers=self.headers)

        rv = self.tester.delete(
            '/api/v1/meals/1', content_type="application/json",headers=self.headers)
        self.assertIn("Only an admin can delete a meal",rv.data.decode())









