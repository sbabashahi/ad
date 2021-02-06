import json
from test.test_base import BaseTestCase


class AdTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        data = {
            'username': 'admin',
            'password': '12345',
        }
        resp = self.app.post('user/register', json=data)
        if resp.status_code != 400:
            data = json.loads(resp.data.decode())
            self.header = {'Authorization': 'JWT {}'.format(data['data']['token'])}
            data = {
                'name': 'Category 1',
            }
            resp = self.app.post('category/', json=data, headers=self.header)
        else:
            resp = self.app.post('user/login', json=data)
            data = json.loads(resp.data.decode())
            self.header = {'Authorization': 'JWT {}'.format(data['data']['token'])}

    def test_create_ad_without_authorization(self):
        data = {
            'title': 'my ad',
            'body': 'body of my ad',
            'category': {'id': 1}
        }
        resp = self.app.post('ad/', json=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 403, 'Wrong response code.')
        self.assertEqual(data['message'], 'You have no Authorization', 'Wrong message.')
        self.assertEqual(data['success'], False, 'Wrong response format.')

    def test_create_ad(self):
        data = {
            'title': 'my ad',
            'body': 'body of my ad',
            'category': {'id': 1}
        }
        resp = self.app.post('ad/', json=data, headers=self.header)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201, 'Wrong response code.')
        self.assertIsInstance(data['data'], dict, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')

    def test_list_ad(self):
        resp = self.app.get('ad/')
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200, 'Wrong response code.')
        self.assertIsInstance(data['data'], list, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')
        self.assertEqual(data['total'], 1, 'Wrong response.')

    def test_list_my_ad(self):
        resp = self.app.get('ad/', headers=self.header)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200, 'Wrong response code.')
        self.assertIsInstance(data['data'], list, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')
        self.assertEqual(data['total'], 1, 'Wrong response.')
