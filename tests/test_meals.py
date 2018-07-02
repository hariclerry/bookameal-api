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

    def test_get_meals_code(self):
        meal = {"meal_option": "fish and rice","meal_option_price": 5000}
        self.tester.post('/api/v1/meals/',data=meal,content_type="application/json")
        rv = self.tester.get('/api/v1/meals/',content_type="application/json",headers=self.headers)
        self.assertEqual(rv.status_code, 200)

    def test_get_meals_data(self):
        rv = self.tester.get('/api/v1/meals/')
        self.assertTrue(isinstance(rv.data, object))

    def test_post_meals(self):
        meal = json.dumps(
            {"meal_option": "tomatoes and rice", "meal_option_price": 8000})
        rv = self.tester.post(
            '/api/v1/meals/', content_type="application/json", data=meal,headers=self.headers)
        self.assertIn("tomatoes and rice", rv.data.decode())


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
                          content_type="application/json", data=meal) #headers=self.headers
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
            '/api/v1/meals/1', content_type="application/json") #headers=self.headers
        self.assertTrue(rv.status_code, 200)









