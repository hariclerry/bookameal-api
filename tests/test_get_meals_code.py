import unittest
import pytest
from bookameal import app
from flask import json,jsonify
from flask_jwt_extended import create_access_token


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_meals_code(self):
        user = (
            {"email": "admin@bookameal.com", "password": "12345"})
        response = self.app.post('/api/v1/auth/login',
                                      content_type="application/json", data=user)

        # access_token = create_access_token('loggedin_user')
        print(response.response)
        access_token = (response.response['access_token'])
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        rv = self.app.get('/api/v1/meals/', headers=access_token)
        self.assertEqual(rv.status_code, 200)


# test_client = app.test_client()
#     access_token = create_access_token('testuser')
#     headers = {
#         'Authorization': 'Bearer {}'.format(access_token)
#     }
