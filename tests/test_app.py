import unittest
import pytest
from bookameal import app
from flask import json


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_login(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "default"})

        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 401)
        self.assertIn("Invalid login credentials", rv.data.decode())

    def test_signup(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("access_token", rv.data.decode())

    def test_signup_with_wrong_credentials(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "different"})
        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("Passwords don't match!", rv.data.decode())

    def test_get_meals(self):
        rv = self.app.get('/api/v1/meals/')
        self.assertEqual(rv.status_code, 200)

    def test_post_meals(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.app.post(
            '/api/v1/meals/', content_type="application/json", data=meal)
        self.assertIn("tomatoes and rice", rv.data.decode())

    def test_put_meals(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.app.put('/api/v1/meals/0',
                          content_type="application/json", data=meal)

        self.assertNotIn("Matooke with g-nuts", rv.data.decode())

    def test_delete_meal(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.app.post('/api/v1/meals/',
                      content_type="application/json", data=json.dumps(meal))
        rv = self.app.delete(
            '/api/v1/meals/1', content_type="application/json")
        self.assertNotIn("Fish", rv.data.decode())

    def test_create_menu(self):
        menu = json.dumps(
            {"date": "2018-9-7", "menu": ["gnuts and pilao", "milk and bread"]})

        rv = self.app.post('/api/v1/menu',
                           content_type="application/json", data=menu)
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Menu has been created", rv.data.decode())

    def test_get_menu(self):
        menu = json.dumps(
            {"date": "2018-9-7", "menu": ["fish and matooke", "milk and bread"]})

        self.app.post('/api/v1/menu',
                      content_type="application/json", data=menu)
        rv = self.app.get('/api/v1/menu', content_type="application/json")
        print(rv.data.decode())
        # these two tests are similar, but implemented in a diffrent fashion
        assert b"fish and matooke" in rv.data
        self.assertIn("fish and matooke", rv.data.decode())

    def test_post_orders(self):
        # first sign up to put some mail in session
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})
        self.app.post('/api/v1/auth/signup',
                      content_type="application/json", data=user)
        # Now create an order, with the mail in session
        orders = ({"date": "2018-7-1", "meal_option": "cassava and milk"})
        rv = self.app.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders))
        self.assertIn("Order has been created", rv.data.decode())

    def test_get_order(self):
        rv = self.app.get('/api/v1/orders')
        self.assertTrue(rv.status_code, 200)
