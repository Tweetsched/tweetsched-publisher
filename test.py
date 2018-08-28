from base64 import b64encode
from app import app
import unittest
from mock import patch
import os
import json
from twython import Twython

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        os.environ['SERVICE_KEY'] = 'test-key'
        os.environ['SERVICE_PASS'] = 'test-secret'
        os.environ['APP_KEY'] = 'test-key'
        os.environ['APP_SECRET'] = 'test-secret'
        os.environ['OAUTH_TOKEN'] = 'test-oauth-token'
        os.environ['OAUTH_TOKEN_SECRET'] = 'test-oauth-token-secret'

    @patch('app.Twython.update_status')
    def test_publish_tweet(self, update_status_mock):
        update_status_mock.return_value = True

        auth = (os.environ['SERVICE_KEY'] + ':' + os.environ['SERVICE_PASS']).encode('utf-8')
        headers = {
            'Authorization': 'Basic ' + b64encode(auth).decode()
        }
        rv = self.app.post('/api/v1/tweets',
                           data=json.dumps(dict(id = 3, message = 'test tweet', profileId = '1')),
                           content_type = 'application/json',
                           headers=headers)

        self.assertEqual(rv.status_code, 200)
        self.assertEqual(update_status_mock.call_count, 1)
        update_status_mock.assert_called_once()

    def test_404(self):
        auth = (os.environ['SERVICE_KEY'] + ':' + os.environ['SERVICE_PASS']).encode('utf-8')
        headers = {
            'Authorization': 'Basic ' + b64encode(auth).decode()
        }
        rv = self.app.get('/i-am-not-found', headers=headers)
        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()
