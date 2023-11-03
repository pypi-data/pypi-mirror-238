import json
import unittest
from unittest import mock
from ..FlaskMain import app, set_frigg_responses  # Import your Flask app
from flask import Flask


class TestKodiakEndpointLocate(unittest.TestCase):
    def setUp(self):
        set_frigg_responses(True)
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_locate_endpoint_with_successful_mDNS_scan(self):
        # Test the endpoint when the mDNS scan is successful
        response = self.app.get('/kodiak/locate')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Success', data)
        self.assertIsInstance(data['Success'], list)
        self.assertTrue(all(isinstance(ip, str) for ip in data['Success']))

    # def test_locate_endpoint_with_failed_mDNS_scan(self):
    #     # Test the endpoint when the mDNS scan fails
    #     with unittest.mock.patch('..FlaskMain.find_kodiak_ip_addresses', side_effect=Exception("Test Error")):
    #         response = self.app.get('/kodiak/locate')
    #         data = json.loads(response.data)
    #
    #         self.assertEqual(response.status_code, 200)
    #         self.assertIn('Error', data)
    #         self.assertEqual(data['Error'], "Error whilst starting MDNS discovery!")

if __name__ == '__main__':
    unittest.main()
