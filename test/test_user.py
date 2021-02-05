import json
from test.test_base import BaseTestCase


class MyTest(BaseTestCase):

    def test_register(self):
        data = {
            'username': 'saeed',
            'password': '12345'
        }
        resp = self.app.post('user/register', json=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200, 'Wrong response code.')
        self.assertIsInstance(data['data'], dict, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')

    def test_register_again(self):
        data = {
            'username': 'saeed',
            'password': '12345'
        }
        resp = self.app.post('user/register', json=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 400, 'Wrong response code.')
        self.assertEqual(data['message'], 'A user with this data exist.', 'Wrong response message.')
        self.assertEqual(data['success'], False, 'Wrong response format.')

    def test_register_login(self):
        data = {
            'username': 'saeed',
            'password': '12345'
        }
        resp = self.app.post('user/login', json=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200, 'Wrong response code.')
        self.assertIsInstance(data['data'], dict, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')
