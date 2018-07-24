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
        self.url = 'api/v1/orders'
        self.menu_url = 'api/v1/menu'
        self.meal_url = 'api/v1/meals/'

    def tearDown(self):
        db.drop_all()

    # Test order can be created
    def test_creating_an_order(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal,
            headers=self.headers)

        menu = json.dumps({"date": "2018-09-07","name":"supper", "menu": [1]})
        self.tester.post(
            self.menu_url,
            content_type="application/json",
            data=menu,
            headers=self.headers)

        orders = (
            {"customer_id": 1, "date":"2018-09-07","menu_category":"supper",
             "meal_option": 1,"order_number":1})
        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=json.dumps(orders),
            headers=self.headers)
        self.assertIn("Order has been created", rv.data.decode())
        self.assertTrue(rv.status_code, 200)

    # Test the get method on orders actually returns the orders
    def test_get_orders(self):
        rv = self.tester.get(
            self.url,
            content_type="application/json",
            headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    # Test order cannot be created with wrong date format
    def test_create_order_with_wrong_date_format(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal,
            headers=self.headers)


        menu = json.dumps({"date": "2018-09-07","name":"dinner", "menu": [1]})
        self.tester.post(
            self.menu_url,
            content_type="application/json",
            data=menu,
            headers=self.headers)

        orders = (
            {"customer_id": 1, "date": "2018-09-7","menu_category":"dinner",
            "meal_option": 1,"order_number":1})

        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=json.dumps(orders),
            headers=self.headers)
        self.assertIn("The meal provided is not in the dinner menu for date 2018-09-7",
         rv.data.decode())

    # # Test you cannot create an order with a meal not on the menu
    def test_create_order_with_wrong_meal_not_in_menu(self):
        meal1 = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal1,
            headers=self.headers)

        meal2 = json.dumps(
            {"meal_option": "fish and matooke", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal2,
            headers=self.headers)

        menu = json.dumps({"date": "2018-09-07","name":"lunch", "menu": [1]})
        self.tester.post(
            self.menu_url,
            content_type="application/json",
            data=menu,
            headers=self.headers)

        orders = (
            {"customer_id": 1, "date": "2018-09-07","menu_category":"lunch",
             "meal_option": 2,"order_number":1})
        rv = self.tester.post(
            self.url,
            content_type="application/json",
            data=json.dumps(orders),
            headers=self.headers)
        self.assertIn(
            "The meal provided is not in the lunch menu for date 2018-09-07",
            rv.data.decode())

    # # Test order can be edited
    def test_order_can_be_edited(self):
        meal1 = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal1,
            headers=self.headers)

        meal2 = json.dumps(
            {"meal_option": "fish and matooke", "meal_option_price": 8000})
        self.tester.post(
            self.meal_url,
            content_type="application/json",
            data=meal2,
            headers=self.headers)

        menu = json.dumps({"date": "2018-09-07","name":"lunch", "menu": [1, 2]})
        rv = self.tester.post(
            self.menu_url,
            content_type="application/json",
            data=menu,
            headers=self.headers)

        order = (
            {"customer_id": 1, "date": "2018-09-07","menu_category":"lunch",
             "meal_option": 1,"order_number":1})
        self.tester.post(
            self.url,
            content_type="application/json",
            data=json.dumps(order),
            headers=self.headers)

        edited_order = (
            {"customer_id": 1, "date": "2018-09-07","menu_category":"lunch",
             "meal_option": 2,"order_number":1})

        rv = self.tester.put(
            self.url+'/1',
            content_type="application/json",
            data=json.dumps(edited_order),
            headers=self.headers)

        self.assertIn("Order has been edited", rv.data.decode())
