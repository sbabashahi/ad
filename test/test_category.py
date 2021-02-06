import json
from test.test_base import BaseTestCase


class CategoryTest(BaseTestCase):

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
        else:
            resp = self.app.post('user/login', json=data)
            data = json.loads(resp.data.decode())
            self.header = {'Authorization': 'JWT {}'.format(data['data']['token'])}

    def test_create_category_without_authorization(self):
        data = {
            'name': 'Category 1',
        }
        resp = self.app.post('category/', json=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 403, 'Wrong response code.')
        self.assertEqual(data['message'], 'You have no Authorization', 'Wrong message.')
        self.assertEqual(data['success'], False, 'Wrong response format.')

    def test_create_category(self):
        data = {
            'name': 'Category 1',
        }
        resp = self.app.post('category/', json=data, headers=self.header)
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 201, 'Wrong response code.')
        self.assertIsInstance(data['data'], dict, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')

    def test_list_category(self):
        resp = self.app.get('category/')
        data = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 200, 'Wrong response code.')
        self.assertIsInstance(data['data'], list, 'Wrong response format.')
        self.assertEqual(data['success'], True, 'Wrong response format.')
        self.assertEqual(data['total'], 1, 'Wrong response.')
