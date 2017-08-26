import unittest
import os
import re
import json
import base64
from werkzeug.datastructures import Headers
from app import create_app, db

class BucketlistItemsTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(self)
        db.create_all()
        self.token =''
        #User Registration and login details
        self.user_registration = {"username" : "emugaya",
                                  "password" : "Jinja@1234"}
        #Register and login user_registration
        res = self.client.post("/api/v1/auth/register/", data=self.user_registration)
        resp = self.client.post("/api/v1/auth/login/", data=self.user_registration)
        data = json.loads(resp.data.decode())
        self.token = data['token']
        self.headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+"unused").encode('ascii')).decode('ascii')}

        # Bucektlist initialization
        self.bucketlist = {'name': "Join Andela"}
        self.bucketlist_1 = {"name" :"Join Andela Uganda"}
        self.bucketlist_2 = {"name" : "Attend Orientation and P&C Clinic"}

        #Create items in bucketlist
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        #Bucekt list items
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
        #variable for updating item status to True
        self.item_update_true = {"done" : True}
        #Variable for updating item name
        self.item_name_new = {"item_name" : "Complete Bootcamp CP1, Make presentation and Get selected"}

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_new_item_in_bucket_list(self):
        """ Test API can create new items in the bucket."""
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item1, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item2, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item3, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item4, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item5, headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_update_a_bucket_list_item(self):
        """ Test API can update items in the bucket list. """
        # Test Update status from False to True
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item1, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item2, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item3, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item4, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item5, headers=self.headers)
        res = self.client.put("api/v1/bucketlists/2/items/4",data =self.item_update_true, headers=self.headers)
        self.assertEqual(res.status_code, 204)
        #Test to update item_name
        res = self.client.put("api/v1/bucketlists/2/items/4",data =self.item_name_new, headers=self.headers)
        self.assertEqual(res.status_code, 204)

    def test_delete_an_item_from_a_bucket_list(self):
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item1, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item2, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item3, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item4, headers=self.headers)
        res = self.client.post("api/v1/bucketlists/2/items/",data =self.bucketlist_item5, headers=self.headers)
        res = self.client.put("api/v1/bucketlists/2/items/4",data =self.item_update_true, headers=self.headers)
        res = self.client.delete("api/v1/bucketlists/2/items/4", headers=self.headers)
        self.assertEqual(res.status_code, 201)

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
