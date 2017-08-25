import unittest
import os
import re
import json
import base64
from werkzeug.datastructures import Headers
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

        self.user_registration = {"username" : "emugaya",
                                  "password" : "Jinja@1234"}

        self.wrong_username = {"username" : "emugay",
                                  "password" : "Jinja@1234"}
        self.no_username_supplied = {"username" : "",
                                  "password" : "Jinja@1234"}
        self.no_password_supplied = {"username" : "mmmmm",
                                  "password" : ""}
        with self.app.app_context():
            # create all tables
            db.create_all()


    def test_user_registration_success(self):
        """ Test user can register succesfully. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "user created succesfully")

    def test_user_registration_unsuccessful_with_no_username(self):
        """ Test user registration fails when no username is supplied"""
        res = self.client().post("/api/v1/auth/register/", data=self.no_username_supplied)
        self.assertEqual(res.status_code,200)
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Username and password must be supplied")

    def test_user_registration_unsuccessful_with_no_password(self):
        """ Test user registration fails when no password is supplied. """
        res = self.client().post("/api/v1/auth/register/", data=self.no_password_supplied)
        self.assertEqual(res.status_code,200)
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Username and password must be supplied")

    def test_user_login_succesful(self):
        """ Test user can login into system and token is generated"""
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        res = self.client().post("/api/v1/auth/login/", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.message = data['message'];
        self.token = data['token']
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.token)
        self.assertEqual(self.message,"Successfully logged in.")

    def test_user_login_unsuccesful_with_wrong_username(self):
        """ Test Error message is returned when wrong username is supplied"""
        res = self.client().post("/api/v1/auth/login/", data=self.no_username_supplied)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'],"Invalid username or password")

    def test_user_login_unsuccesful_with_wrong_password(self):
        """ Test Error message is returned when wrong password is supplied"""
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        res = self.client().post("/api/v1/auth/login/", data=self.wrong_username)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'],"Invalid username or password")

    def tearDown(self):
                """Teardown all initialized variables."""
                with self.app.app_context():
                    # pass
                    # drop all tables
                    db.session.remove()
                    db.drop_all()

        # Make the tests conveniently executable
if __name__ == "__main__":
            unittest.main()
