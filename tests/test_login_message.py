import unittest
import pytest
from bookameal import app
from flask import json


class CheckTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_login_message(self):
        user = json.dumps(
            {"email": "nabaasarichard@gmail.com", "password": "somepass"})
        rv = self.app.post('/api/v1/auth/login',
                           content_type="application/json", data=user)
        self.assertIn("Invalid login credentials", rv.data.decode())