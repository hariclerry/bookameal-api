import unittest
import pytest
from bookameal import app
from flask import json,jsonify
from flask_jwt_extended import create_access_token


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client()
        app.config['TESTING'] = True
        with self.tester as c:
            with c.session_transaction() as sess:
                sess['email'] = 'admin@bookameal.com'

        user = {"email": "admin@bookameal.com", "password": "12345"}
        response = self.tester.post('/api/v1/auth/login',
                                      content_type="application/json", data=json.dumps(user))
        result = json.loads(response.data.decode())
        access_token = result['access_token']
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

    def tearDown(self):
        pass


    def test_post_orders(self):
        orders = (
            {"date": "2018-09-07", "meal_option": 1, "customer_id": 1})
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







