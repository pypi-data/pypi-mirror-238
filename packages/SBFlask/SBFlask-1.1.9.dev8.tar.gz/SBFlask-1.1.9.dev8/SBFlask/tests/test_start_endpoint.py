import json
import unittest
from ..FlaskMain import app, set_frigg_responses  # Import your Flask app


class TestKodiakStartEndpoint(unittest.TestCase):
    def setUp(self):
        set_frigg_responses(True)
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_start_endpoint_with_valid_data(self):
        # Test the endpoint with valid data
        data = {
            "ipaddress": "192.168.1.247",
            "key": "your_api_key"
        }
        response = self.app.post('/kodiak/start', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Success', data)

    def test_start_endpoint_with_missing_ip(self):
        # Test the endpoint with missing IP address
        data = {
            "key": "your_api_key"
        }
        response = self.app.post('/kodiak/start', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Missing IP address")

    def test_start_endpoint_with_missing_data(self):
        # Test the endpoint with missing data
        response = self.app.post('/kodiak/start')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Request not of type JSON")

    def test_start_endpoint_with_wrong(self):
        # Test the endpoint with wrong data
        data = "key: your_api_key"
        response = self.app.post('/kodiak/start', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Request not of correct JSON format")

if __name__ == '__main__':
    unittest.main()
