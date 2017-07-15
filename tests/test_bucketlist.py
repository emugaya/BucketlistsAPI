import unittest
import os
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
        res = self.client().get('/api/v1/hello')
        self.assertEqual(res.status_code, 200)
        self.assertIn('{"hello":"world"}', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
