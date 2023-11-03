import json
import logging
import unittest
from unittest.mock import MagicMock, patch, call
from SBFlask.FlaskMain import app, set_frigg_responses, KodiakController  # Import your Flask app


class TestKodiakStartEndpointLive(unittest.TestCase):
    def setUp(self):
        set_frigg_responses(False)
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_start_bad_IP(self):
        data = {
            "ipaddress": "0.0.0.0", # An IP that should never work
            "key": "your_api_key"
        }

        # Mock the database response as we don't need it at the moment
        KodiakController.db.get_kodiak_db = MagicMock(return_value=["0.0.0.0", '', '', "your_api_key"])

        response = self.app.post('/kodiak/start', json=data)
        data = json.loads(response.data)

        print(data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Error', data)


if __name__ == '__main__':
    unittest.main()
