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


    def test_post_orders(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)

        menu = json.dumps({"date":"2018-09-07","menu":[1]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        orders = (
            { "customer_id": 1, "date": 1, "meal_option": 1})
        rv = self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders),headers=self.headers)
        self.assertIn("Order has been created", rv.data.decode())

    def test_create_meal_code(self):
        data = ({"meal_option": "fish and rice", "meal_option_price": 16000})
        rv = self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=data,headers=self.headers)
        self.assertTrue(rv.status_code, 200)


    def test_post_order_status(self):
        orders = ({"date": "2018-7-1", "meal_option": 1,"customer_id":1})
        rv = self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders),headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    def test_get_order(self):
        rv = self.tester.get('/api/v1/orders',content_type="application/json",headers=self.headers)
        self.assertTrue(rv.status_code, 200)

    def test_post_orders_with_wrong_date_id(self):
        meal = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)

        menu = json.dumps({"date":"2018-09-07","menu":[2]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        orders = (
            { "customer_id": 1, "date": 1, "meal_option": 1})
        rv = self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders),headers=self.headers)
        self.assertIn("Date with id 1 not found", rv.data.decode())


    def test_post_orders_with_wrong_meal_not_in_menu(self):
        meal1 = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal1,headers=self.headers)

        meal2 = json.dumps(
            {"meal_option": "fish and matooke", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal2,headers=self.headers)

        menu = json.dumps({"date":"2018-09-07","menu":[1]})
        self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        orders = (
            { "customer_id": 1, "date": 1, "meal_option": 2})
        rv = self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders),headers=self.headers)
        self.assertIn("The meal provided is not in the menu for date with id 1", rv.data.decode())

    def test_put_order(self):
        meal1 = json.dumps(
            {"meal_option": "fish and rice", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal1,headers=self.headers)

        meal2 = json.dumps(
            {"meal_option": "fish and matooke", "meal_option_price": 8000})
        self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal2,headers=self.headers)

        menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
        rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)

        order = (
            {"customer_id": 1, "date": 1, "meal_option": 1})
        self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(order),headers=self.headers)

        edited_order = (
            {"customer_id": 1, "date": 1, "meal_option": 2})

        rv = self.tester.put(
            '/api/v1/orders/1', content_type="application/json", data=json.dumps(edited_order),headers=self.headers)

        self.assertIn("Order has been edited",rv.data.decode())














