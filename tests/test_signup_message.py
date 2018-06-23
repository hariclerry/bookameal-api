import unittest
import pytest
from bookameal import app
from flask import json


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_signup_message(self):
        user = json.dumps({"name": "Nabaasa Richard", "location": "Kampala",
                           "email": "nabaasa@gmail.com", "password": "default", "password_conf": "default"})

        rv = self.app.post('/api/v1/auth/signup',
                           content_type="application/json", data=user)
        self.assertIn("welcome, thanks for signing up", rv.data.decode())
