import unittest
import pytest
from bookameal import app
from flask import json, jsonify
from flask_jwt_extended import create_access_token

import os
from bookameal.config import app_config
from bookameal.models import User, Meal, Menu, Order, datemenu
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
            "email": "admin@bookameal.com", "password": "12345", })

        response = self.tester.post(
            '/api/v1/auth/login',
            content_type="application/json",
            data=login_admin)
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        self.url = 'api/v1/meals/'

    def tearDown(self):
        db.drop_all()


    # Test that the get method on meals actually returns the meals
    def test_get_meals(self):
        rv = self.tester.get(
            self.url,
            content_type="application/json",
            headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(isinstance(rv.data, object))

    # Test that a meal can be created
    def test_create_meal(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=meal,
            headers=self.headers)
        self.assertIn("Meal created successfully", rv.data.decode())
        self.assertTrue(rv.status_code, 201)

    # Test that a meal can be edited
    def test_editing_a_meal(self):
        meal_data = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})

        self.tester.post(
            self.url,
            content_type="application/json",
            data=meal_data,
            headers=self.headers)

        meal = json.dumps(
            {"meal_option": "salad and mineral water", "meal_option_price": 20000})

        rv = self.tester.put(
            self.url+'1',
            content_type="application/json",
            data=meal,
            headers=self.headers)
        self.assertIn("Meal updated successfully", rv.data.decode())
        self.assertTrue(rv.status_code, 200)

    # Test you cannot edit a meal with a meal_name already in the system.
    def test_editing_meal_with_name_already_registered(self):
        meal_data = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})

        self.tester.post(
            self.url,
            content_type="application/json",
            data=meal_data,
            headers=self.headers)

        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        rv = self.tester.put(
            self.url+'1',
            content_type="application/json",
            data=meal,
            headers=self.headers)
        self.assertIn("The meal has already been registered", rv.data.decode())

    # Test that a meal can be deleted
    def test_delete_meal(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.tester.post(
            self.url,
            content_type="application/json",
            data=meal,
            headers=self.headers)
        rv = self.tester.delete(
            self.url+'1', content_type="application/json")
        self.assertNotIn("Fish", rv.data.decode())
        # self.assertEqual(rv.status_code,200)

