import unittest
import os

from init_test_db import init_db
from app import app


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        init_db()

    @classmethod
    def tearDownClass(cls):
        os.remove('test.db')

    def setUp(self):
        self.app = app.test_client()
