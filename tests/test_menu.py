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


    def test_create_menu(self):
    	menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
    	rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)
    	self.assertIn("Menu has been created",rv.data.decode())

    def test_create_menu_code(self):
    	menu = json.dumps({"date":"2018-09-07","menu":[1,2]})
    	rv = self.tester.post('/api/v1/menu',content_type="application/json",data=menu,headers=self.headers)


    def test_get_menu(self):
    	# the meal option "tomatoes and rice" comes from the meals created in the 'test_meals.py' file
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        # these two tests are similar, but implemented in a diffrent fashion
        assert b"tomatoes and rice" in rv.data
        self.assertIn("tomatoes and rice", rv.data.decode())

    def test_get_menu_code(self):
        menu = json.dumps(
            {"date": "2018-09-07", "menu": ["fish and matooke", "milk and bread"]})

        self.tester.post('/api/v1/menu',
                      content_type="application/json", data=menu,headers=self.headers)
        rv = self.tester.get('/api/v1/menu', content_type="application/json",headers=self.headers)
        self.assertTrue(rv.status_code, 200)







