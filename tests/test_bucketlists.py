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
        self.headers={'Authorization': 'Basic ' + base64.b64encode((self.token+":"+\
                                        "unused").encode('ascii')).decode('ascii')}

        self.bucketlist_no_name = {"name":""}
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

    def test_bucketlist_creation_succesful(self):
        """Test API can create a new bucket list. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        self.assertEqual(res.status_code, 201)
    
    def test_creating_duplicate_buckets_unsuccesful(self):
        """Test API can't create duplicate bucketlists. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist,headers=self.headers)
        self.assertEqual(res.status_code, 409) 
    
    def test_prevent_creating_bucket_list_with_out_name(self):
        res =self.client.post("/api/v1/bucketlists/", data=self.bucketlist_no_name, headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Please provide a name for your bucketlist")

    def test_listing_all_created_bucket_lists_with_pagination(self):
        """Test API can list buckets created. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        res= self.client.get('/api/v1/bucketlists/', headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['pages'], 1)

    def test_get_single_bucket_list(self):
        """ Test API return a single bucket list with it's items. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        res = self.client.get("/api/v1/bucketlists/1",headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_get_no_existing_bucket(self):
        res = self.client.get("/api/v1/bucketlists/1",headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'],  "Bucket 1 Doesn't Exist")

    def test_editing_single_bucket_list(self):
        """ Test API can update a single bucket list. """
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.put("/api/v1/bucketlists/1", data=self.bucketlist_1, headers=self.headers)
        self.assertEqual(res.status_code, 204)
        res = self.client.get("/api/v1/bucketlists/1", headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(data['name'], self.bucketlist_1['name'])

    def test_editing_fails_when_name_is_empty(self):
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.put("/api/v1/bucketlists/1", data=self.bucketlist_no_name, headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Please provide a new name for your bucketlist")

    def test_editing_fails_when_non_existing_bucket_id_is_supplied(self):
        res = self.client.put("/api/v1/bucketlists/1", data=self.bucketlist_2, headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "The Buckelist 1 provided doesn't exist ....")

        
    def test_delete_single_bucket_lists_(self):
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_1,headers=self.headers)
        res = self.client.post("/api/v1/bucketlists/",data=self.bucketlist_2,headers=self.headers)
        """ Test API can delete a single bucket list. """
        res = self.client.delete("api/v1/bucketlists/1",headers=self.headers)
        self.assertEqual(res.status_code,201)

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
