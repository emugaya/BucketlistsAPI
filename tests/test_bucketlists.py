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

    def test_bucketlist_creation(self):
        """Test API can create a new bucket list. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        self.assertEqual(res.status_code, 200)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        self.assertEqual(res.status_code, 200)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_listing_all_created_bucket_lists(self):
        """Test API can list buckets created. """
        res= self.client.get('/api/v1/bucketlists/', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_single_bucket_list(self):
        """ Test API return a single bucket list with it's items. """
        res = self.client.get("/api/v1/bucketlists/1",headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_update_single_bucket_list(self):
        """ Test API can update a single bucket list. """
        res = self.client.put("/api/v1/bucketlists/2", data=self.bucketlist2, headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_delete_single_bucket_list(self):
        """ Test API can delete a single bucket list. """
        res = self.client.delete("api/v1/bucketlists/3",headers=self.headers)
        self.assertEqual(res.status_code,200)

    def tearDown(self):
        """Teardown all initialized variables."""
            # db.session.remove()
            # db.drop_all()
        with self.app.app_context():
            # pass
            # drop all tables
            db.session.remove()
            db.drop_all()

    # Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
