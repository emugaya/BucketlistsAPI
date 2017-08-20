import unittest
import os
import re
import json
from app import create_app, db

class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        # self.bucketlist = {"name": "Apply to Andela"}
        self.token = ''
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
        self.test = ''
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_helloworld(self):
        """Test API can return hello world"""
        # rv = self.client().get('/api/v1/hello')
        # self.assertEqual(rv.status_code, 200)
        # result_in_json = json.dumps(rv.data.decode('utf-8').replace("'", "\""))

        # result_in_json = result_in_json.replace("\\n","")
        # result_in_json = result_in_json.replace('\\','')

        # self.assertIn('"hello": "world"', result_in_json)
        # print(rv.data)
        pass
    def test_user_registration(self):
        """ Test user can register a user. """
        res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        self.assertEqual(res.status_code,200)
        self.test = 'Uganda'

    def test_user_login(self):
        """ Test user can login into system and token is generated"""
        # res = self.client().post("/api/v1/auth/register/", data=self.user_registration)
        # self.assertEqual(res.status_code,200)
        res = self.client().post("/api/v1/auth/login", data=self.user_registration)
        data = json.loads(res.data.decode())
        print('..................................................................')
        print (data)
        self.assertEqual('Uganda',self.test)
        self.token = data['token']
        self.assertEqual(res.status_code, 200)

    def test_bucketlist_creation(self):
        """Test API can create a new bucket list. """
        res = self.client().post("/api/v1/bucketlists/", data=self.bucketlist)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("/api/v1/bucketlists/",data=self.bucketlist_1)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("/api/v1/bucketlists/",data=self.bucketlist_2)
        self.assertEqual(res.status_code, 200)

    def test_listing_all_created_bucket_lists(self):
        """Test API can list buckets created. """
        res= self.client().get('/api/v1/bucketlists/')
        self.assertEqual(res.status_code, 200)

    def test_get_single_bucket_list(self):
        """ Test API return a single bucket list with it's items. """
        res = self.client().get("/api/v1/bucketlists/2")
        self.assertEqual(res.status_code, 200)

    def test_update_single_bucket_list(self):
        """ Test API can update a single bucket list. """
        res = self.client().put("/api/v1/bucketlists/2", data=self.bucketlist2)
        self.assertEqual(res.status_code, 200)


    def test_delete_single_bucket_list(self):
        """ Test API can delete a single bucket list. """
        res = self.client().delete("api/v1/bucketlists/3")
        self.assertEqual(res.status_code,200)


    def test_create_new_item_in_bucket_list(self):
        """ Test API can create new items in the bucket."""
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item1)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item2)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item3)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item4)
        self.assertEqual(res.status_code, 200)
        res = self.client().post("api/v1/bucketlists/2/items",data =self.bucketlist_item5)
        self.assertEqual(res.status_code, 200)

    def test_update_a_bucket_list_item(self):
        """ Test API can update items in the bucket list. """
        # Test Update status from False to True
        res = self.client().put("api/v1/bucketlists/2/items/4",data =self.item_update_true)
        self.assertEqual(res.status_code, 200)
        #Test to update item_name
        res = self.client().put("api/v1/bucketlists/2/items/4",data =self.item_name_new)
        self.assertEqual(res.status_code, 200)

    def test_delete_an_item_from_a_bucket_list(self):
        res = self.client().delete("api/v1/bucketlists/2/items/4")
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
