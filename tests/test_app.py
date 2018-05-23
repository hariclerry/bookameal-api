import unittest
import pytest
from bookameal import app
from flask import json


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass
    # test the login status code

    def test_login_code(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 401)
    # test the login message when one logsin with wrong info

    def test_login_message(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertIn("Invalid login credentials", rv.data.decode())
    # test the signup status code

    def test_signup_code(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertEqual(rv.status_code, 201)
    # test the signup token

    def test_signup_token(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("access_token", rv.data.decode())
    # test the signup message

    def test_signup_message(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("welcome, thanks for signing up", rv.data.decode())
    # test signup with wrong credentials

    def test_signup_with_wrong_credentials(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "different"})
        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("Passwords don't match!", rv.data.decode())
    # test get meals code

    def test_get_meals_code(self):
        rv = self.app.get('/api/v1/meals/',)
        self.assertEqual(rv.status_code, 200)
    # test get meals actiually returns data

    def test_get_meals_data(self):
        rv = self.app.get('/api/v1/meals/')
        self.assertTrue(isinstance(rv.data, object))
# test create meal actually creates it

    def test_post_meals(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.app.post(
            '/api/v1/meals/', content_type="application/json", data=meal)
        self.assertIn("tomatoes and rice", rv.data.decode())
# test create meal status code

    def test_post_meals_code(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.app.post(
            '/api/v1/meals/', content_type="application/json", data=meal)
        self.assertTrue(rv.status_code, 200)
# test edit meal actually edits the meal

    def test_put_meals(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.app.put('/api/v1/meals/0',
                          content_type="application/json", data=meal)

        self.assertNotIn("Matooke with g-nuts", rv.data.decode())
# test edit meal status code

    def test_put_meals_code(self):
        meal = json.dumps(
            {"meal_option": "Salad and Mineral water", "meal_option_price": 20000})
        rv = self.app.put('/api/v1/meals/0',
                          content_type="application/json", data=meal)

        self.assertTrue(rv.status_code, 200)
# test delete meal actually deletes the meal

    def test_delete_meal(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.app.post('/api/v1/meals/',
                      content_type="application/json", data=json.dumps(meal))
        rv = self.app.delete(
            '/api/v1/meals/1', content_type="application/json")
        self.assertNotIn("Fish", rv.data.decode())
# test delete meal status code

    def test_delete_meal_code(self):
        meal = json.dumps(
            {"meal_option": "Fish", "meal_option_price": 20000})
        self.app.post('/api/v1/meals/',
                      content_type="application/json", data=json.dumps(meal))
        rv = self.app.delete(
            '/api/v1/meals/1', content_type="application/json")
        self.assertTrue(rv.status_code, 200)
# test create menu actually creates the menu

    def test_create_menu(self):
        menu = json.dumps(
            {"date": "2018-9-7", "menu": ["gnuts and pilao", "milk and bread"]})

        rv = self.app.post('/api/v1/menu',
                           content_type="application/json", data=menu)
        self.assertIn("Menu has been created", rv.data.decode())
# test create menu status code

    def test_create_menu_code(self):
        menu = json.dumps(
            {"date": "2018-9-7", "menu": ["gnuts and pilao", "milk and bread"]})

        rv = self.app.post('/api/v1/menu',
                           content_type="application/json", data=menu)
        self.assertEqual(rv.status_code, 201)
# test getting menu actually gets them

    def test_get_menu(self):

        rv = self.app.get('/api/v1/menu', content_type="application/json")
        # these two tests are similar, but implemented in a diffrent fashion
        assert b"milk and bread" in rv.data
        self.assertIn("milk and bread", rv.data.decode())
# test get menu status code

    def test_get_menu_code(self):
        menu = json.dumps(
            {"date": "2018-9-7", "menu": ["fish and matooke", "milk and bread"]})

        self.app.post('/api/v1/menu',
                      content_type="application/json", data=menu)
        rv = self.app.get('/api/v1/menu', content_type="application/json")
        self.assertTrue(rv.status_code, 200)

# test create orders actually creates an order and returns the expected message
    def test_post_orders(self):
        # first sign up to put some mail in session
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})
        self.app.post('/api/v1/auth/signup',
                      content_type="application/json", data=user)
        # Now create an order, with the mail in session
        orders = (
            {"date": "2018-7-1", "meal_option": "cassava and milk", "customer_id": 1})
        rv = self.app.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders))
        self.assertIn("Order has been created", rv.data.decode())
# test create order status code

    def test_create_meal_code(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})
        self.app.post('/api/v1/auth/signup',
                      content_type="application/json", data=user)
        data = ({"meal_option": "fish and rice", "meal_option_price": 16000})
        rv = self.app.post(
            '/api/v1/meals/', content_type="application/json", data=data)
        self.assertTrue(rv.status_code, 200)

    def test_post_order_status(self):
        # first sign up to put some mail in session
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasarichard@gmail.com", "password": "default", "password_conf": "default"})
        self.app.post('/api/v1/auth/signup',
                      content_type="application/json", data=user)
        # Now create an order, with the mail in session
        orders = ({"date": "2018-7-1", "meal_option": "cassava and milk"})
        rv = self.app.post(
            '/api/v1/orders', content_type="application/json", data=json.dumps(orders))
        self.assertTrue(rv.status_code, 200)
# test get one order status

    def test_get_order(self):
        rv = self.app.get('/api/v1/orders')
        self.assertTrue(rv.status_code, 200)
