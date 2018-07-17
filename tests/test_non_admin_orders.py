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


    def test_post_orders(self):
        orders = (
            {"date": "2018-09-07", "meal_option": 1, "customer_id": 1})
        rv = self.tester.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders),headers=self.headers)
        self.assertIn("Date should be an integer, not string", rv.data.decode())

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







