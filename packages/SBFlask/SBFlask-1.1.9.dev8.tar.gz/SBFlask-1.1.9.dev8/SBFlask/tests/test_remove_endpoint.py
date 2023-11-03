import json
import unittest
from SBFlask.FlaskMain import app, set_frigg_responses  # Import your Flask app


class TestKodiakRemoveEndpoint(unittest.TestCase):
    def setUp(self):
        set_frigg_responses(True)
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_remove_endpoint_with_valid_ip(self):
        # Test the endpoint with a valid IP address
        data = {
            "ipaddress": "192.168.1.247"
        }
        response = self.app.post(f'/kodiak/remove', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Success', data)

    def test_remove_endpoint_with_bad_format_ip(self):
        # Test the endpoint with a valid IP address
        data = {
            "ipaddress": "192.168.1.247."
        }
        response = self.app.post(f'/kodiak/remove', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Badly formatted IP address value")

    def test_remove_endpoint_with_bad_no_ip(self):
        # Test the endpoint with a valid IP address
        data = {
            "ipaddress": ""
        }
        response = self.app.post(f'/kodiak/remove', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Badly formatted IP address value")

    def test_remove_endpoint_with_bad_args(self):
        # Test the endpoint with a valid IP address
        data = {
            "key": "192.168.1.247"
        }
        response = self.app.post(f'/kodiak/remove', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Missing IP address")

    def test_remove_endpoint_with_missing_ip(self):
        # Test the endpoint with a missing IP address

        data = {
        }
        response = self.app.post(f'/kodiak/remove', json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)
        self.assertEqual(data['Error'], "Request missing args")


if __name__ == '__main__':
    unittest.main()
