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

    def test_helloworld(self):
        """Test API can return hello world"""
        rv = self.client().get('/api/v1/hello')
        self.assertEqual(rv.status_code, 200)
        result_in_json = json.dumps(rv.data.decode('utf-8').replace("'", "\""))

        result_in_json = result_in_json.replace("\\n","")
        result_in_json = result_in_json.replace('\\','')

        self.assertIn('"hello": "world"', result_in_json)
        # print(rv.data)
    def test_user_registration(self):
        pass

    def test_user_login(self):
        pass

    def test_create_a_new_bucket_list(self):
        """Test API can create a new bucket list"""
        self.bucketlist =
        pass

    def test_listing_all_created_bucket_lists(self):
        pass

    def test_get_single_bucket_list(self):
        pass

    def test_update_single_bucket_list(self):
        pass

    def test_delete_single_bucket_list(self):
        pass

    def test_create_new_item_in_bucket_list(self):
        pass

    def test_update_a_bucket_list_item(self):
        pass

    def test_delete_an_item_in_a_bucket_list(self):
        pass

    def tearDown(self):
        """teardown all initialized variables."""
        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
