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
        res = self.client.post("/api/v1/auth/register/", 
                    data=self.user_registration)
        resp = self.client.post("/api/v1/auth/login/", 
                    data=self.user_registration)
        data = json.loads(resp.data.decode())
        self.token = data['token']
        self.headers={'Authorization': 'Basic ' + base64.b64encode((self.token
                        + ":" +"unused").encode('ascii')).decode('ascii')}

        self.bucketlist = {'name': "Join Andela"}


        #Create items in bucketlist
        res = self.client.post("/api/v1/bucketlists/", data=self.bucketlist, \
                                headers=self.headers)
        #Bucekt list items
        self.bucketlist_item1 = {"name": "Apply and Pass Plum test",
                                 "done": False
                                 }
        self.bucketlist_item2 = {"name": "Take Home Study and Finish Labs",
                                 "done": False
                                 }
        self.bucketlist_item3 = {"name" : "Complete Self learning Clinic",
                                 "done": False
                                 }
        self.bucketlist_item4 = {"name" : "Complete Bootcamp CP1",
                                 "done" : False
                                 }
        self.bucketlist_item5 = {"name" : "Complete CP2",
                                 "done" : False
                                 }
        self.bucketlist_item_without_name ={"name":"", "done":"false"}

        self.bucketlist_item_without_done ={"name":"Travel to Kigali", "done":""}

        self.item_update_name_new = {"name" : "Complete Bootcamp CP1",
                             "done": True}

        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_new_item_in_bucket_list(self):
        """ Test API can create new items in the bucket."""
        res = self.client.post("api/v1/bucketlists/1/items/",
                data =self.bucketlist_item1, headers=self.headers)
        self.assertEqual(res.status_code, 201)

    def test_creating_items_with_same_name_unsuccesful(self):
        """ Test API can't create Item with similar name."""
        res = self.client.post("api/v1/bucketlists/1/items/",
            data =self.bucketlist_item1, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        res = self.client.post("api/v1/bucketlists/1/items/",
            data =self.bucketlist_item1, headers=self.headers)
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data.decode())
        self.assertEqual(data['message'], "Item with this name already exits")

    def test_create_new_item_unsuccesfully_with_no_name(self):
        res = self.client.post("api/v1/bucketlists/1/items/",
                data =self.bucketlist_item_without_name, headers=self.headers)
        self.assertEqual(res.status_code, 400)

    def test_update_a_bucket_list_item_succesfully(self):
        """ Test API can update items in the bucket list. """
        # Test Update status from False to True
        res = self.client.post("api/v1/bucketlists/1/items/",
                    data =self.bucketlist_item1, headers=self.headers)
        res = self.client.put("api/v1/bucketlists/1/items/1",
                    data =self.item_update_name_new, headers=self.headers)
        self.assertEqual(res.status_code, 204)

    def test_update_item_unsuccesful_with_no_name(self):
        """Test API does't Allow Updating Name with empty String"""
        res = self.client.post("api/v1/bucketlists/1/items/",
                    data =self.bucketlist_item1, headers=self.headers)
        res = self.client.put("api/v1/bucketlists/1/items/1", 
                    data = self.bucketlist_item_without_name, headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Please Supply Name and done status.")

    def test_update_item_unsuccesful_with_no_done_status(self):
        """Test API does't Allow Updating Name with empty String"""
        res = self.client.post("api/v1/bucketlists/1/items/",
                    data =self.bucketlist_item1, headers=self.headers)
        res = self.client.put("api/v1/bucketlists/1/items/1", 
                    data = self.bucketlist_item_without_done, headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Please Supply Name and done status.")

    def test_delete_an_item_from_a_bucket_list_succesfully(self):
        """ Test API Can Delete Item from Bucket Succesfully"""
        res = self.client.post("api/v1/bucketlists/1/items/",
                    data =self.bucketlist, headers=self.headers)
        res = self.client.delete("api/v1/bucketlists/1/items/1", headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(data["message"], "Item Deleted succesfully")
        self.assertEqual(res.status_code, 200)

    def test_delete_unexisting_item_id_unsuccesful(self):
        """Test API returns 400 if unexisting item_id in request"""
        res = self.client.post("api/v1/bucketlists/1/items/",
                    data =self.bucketlist, headers=self.headers)
        res = self.client.delete("api/v1/bucketlists/1/items/2", headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(data["message"], "Item 2 Doesn't Exist")
        self.assertEqual(res.status_code, 404)

    def test_delete_an_item_from_invalid_bucket_unsuccesful(self):
        """ Test Returns 400 Error invalid bucekt_id in request"""
        res = self.client.post("api/v1/bucketlists/1/items/",
                data =self.bucketlist, headers=self.headers)
        res = self.client.delete("api/v1/bucketlists/12/items/13", headers=self.headers)
        data = json.loads(res.data.decode())
        self.assertEqual(data["message"], "The Bucket 12 passed does not exist")
        self.assertEqual(res.status_code, 404)
    

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
