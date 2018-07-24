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
        self.url = 'api/v1/meals/'

    def tearDown(self):
        db.drop_all()

    # Test get method on meals actually returns the meals
    def test_get_meals(self):
        meal = {"meal_option": "fish and rice", "meal_option_price": 5000}
        self.tester.post(
            self.url,
            data=meal,
            content_type="application/json")
        rv = self.tester.get(
            self.url,
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(rv.status_code, 401)

    # Test meal cannot be created by a user who is not a caterer
    def test_create_meals(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=meal,
            headers=self.headers)
        self.assertIn("Only an admin can create a meal", rv.data.decode())

    # Test a user who is not an admin cannot eddit a meal
    def test_edit_a_meal(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.tester.put(
            self.url+'1',
            content_type="application/json",
            data=meal,
            headers=self.headers)
        self.assertNotIn("Matooke with g-nuts", rv.data.decode())
        self.assertTrue(rv.status_code, 401)

    def test_meal_can_be_deleted(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.tester.post(
            self.url,
            content_type="application/json",
            data=meal,
            headers=self.headers)
        rv = self.tester.delete(
            self.url+'1', content_type="application/json",headers=self.headers)
        self.assertNotIn("Fish", rv.data.decode())
        self.assertTrue(rv.status_code, 200)
        self.assertIn("Only an admin can delete a meal", rv.data.decode())


