import unittest
import os
import re
import json
import base64
from werkzeug.datastructures import Headers
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # self.bucketlist = {"name": "Apply to Andela"}
        self.token = ''
        self.status = ''
        self.bucketlist = {'name': "Join Andela"}
        self.bucketlist_1 = {"name" :"Join Andela Uganda"}
        self.bucketlist_2 = {"name" : "Attend Orientation and P&C Clinic"}
        self.bucketlist_item1 = {"item_name": "Apply and Pass Plum test",
                                 "done": False
                                 }
        self.bucketlist_item2 = {"item_name": "Take Home Study and Finish Labs",
                                 "done": False
                                 }
        self.bucketlist_item3 = {"item_name" : "Complete Self learning Clinic",
                                 "done": False
                                 }
        self.bucketlist_item4 = {"item_name" : "Complete Bootcamp CP1",
                                 "done" : False
                                 }
        self.bucketlist_item5 = {"item_name" : "Complete CP2",
                                 "done" : False
                                 }
        # Variables for Update Bucket list
        self.bucketlist2 = {"name": "Become a Fellow at Andela"}
        #variable for updating item status to True
        self.item_update_true = {"done" : True}
        #Variable for updating item name
        self.item_name_new = {"item_name" : "Complete Bootcamp CP1, Make presentation and Get selected"}
        # binds the app to the current context
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

    # def test_helloworld(self):
        """Test API can return hello world"""
        # rv = self.client().get('/api/v1/hello')
        # self.assertEqual(rv.status_code, 200)
        # result_in_json = json.dumps(rv.data.decode('utf-8').replace("'", "\""))

        # result_in_json = result_in_json.replace("\\n","")
        # result_in_json = result_in_json.replace('\\','')

        # self.assertIn('"hello": "world"', result_in_json)
        # print(rv.data)
        # pass
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
        self.assertEqual(data['error_message'], "Username and password must be supplied")

    def test_user_registration_unsuccessful_with_no_password(self):
        """ Test user registration fails when no password is supplied. """
        res = self.client().post("/api/v1/auth/register/", data=self.no_password_supplied)
        self.assertEqual(res.status_code,200)
        data = json.loads(res.data.decode())
        self.assertEqual(data['error_message'], "Username and password must be supplied")


    def test_user_login_succesful(self):
        """ Test user can login into system and token is generated"""
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.message = data['message'];
        self.token = data['token']
        self.status = data['status']
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.token)
        self.assertEqual(self.message,"Successfully logged in.")
        self.assertEqual(self.status, "success")


    def test_user_login_unsuccesful_with_wrong_username(self):
        """ Test Error message is returned when wrong username is supplied"""
        res = self.client().post("/api/v1/auth/login", data=self.no_username_supplied)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error_message'],"Invalid username or password")

    def test_user_login_unsuccesful_with_wrong_password(self):
        """ Test Error message is returned when wrong password is supplied"""
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        res = self.client().post("/api/v1/auth/login", data=self.wrong_username)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error_message'],"Invalid username or password")

    def test_bucketlist_creation(self):
        """Test API can create a new bucket list. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().post("/api/v1/bucketlists/", data=self.bucketlist, headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_listing_all_created_bucket_lists(self):
        """Test API can list buckets created. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res= self.client().get('/api/v1/bucketlists/', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_get_single_bucket_list(self):
        """ Test API return a single bucket list with it's items. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().get("/api/v1/bucketlists/2",headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_single_bucket_list(self):
        """ Test API can update a single bucket list. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().put("/api/v1/bucketlists/2", data=self.bucketlist2, headers=headers)
        self.assertEqual(res.status_code, 200)


    def test_delete_single_bucket_list(self):
        """ Test API can delete a single bucket list. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().delete("api/v1/bucketlists/3",headers=headers)
        self.assertEqual(res.status_code,200)


    def test_create_new_item_in_bucket_list(self):
        """ Test API can create new items in the bucket."""
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item1, headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item2, headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item3, headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item4, headers=headers)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item5, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_a_bucket_list_item(self):
        """ Test API can update items in the bucket list. """
        # Test Update status from False to True
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().put("api/v1/bucketlists/2/items/4",data =self.item_update_true, headers=headers)
        self.assertEqual(res.status_code, 200)
        #Test to update item_name
        res = self.client().put("api/v1/bucketlists/2/items/4",data =self.item_name_new, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_delete_an_item_from_a_bucket_list(self):
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        self.token = data['token']
        headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}
        res = self.client().delete("api/v1/bucketlists/2/items/4", headers=headers)
        self.assertEqual(res.status_code, 200)

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
