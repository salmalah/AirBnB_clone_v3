#!/usr/bin/python3
import unittest
from api.v1.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        """
        Set up test client
        """
        self.test_client = app.test_client()

    def test_404_response(self):
        """
        Test 404 response for unknown route
        """
        response = self.test_client.get('/unknown_route')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not found", response.data)

    def test_sample_endpoint(self):
        """
        Test a sample endpoint for successful response
        """
        response = self.test_client.get('/sample_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Sample response data", response.data)

if __name__ == "__main__":
    unittest.main()
