import unittest
import os
from your_flask_app_file import _allowed_file, _diff  # replace with your filename

class TestApp(unittest.TestCase):
    
    def test_allowed_file(self):
        self.assertTrue(_allowed_file('test.jpg'))
        self.assertFalse(_allowed_file('test.txt'))

    def test_diff(self):
        self.assertEqual(_diff(['a', 'b', 'c'], ['b']), ['a', 'c'])
        self.assertEqual(_diff(['a', 'b', 'c'], ['d']), ['a', 'b', 'c'])

# pour les tests d'intégration de Flask, vous pouvez faire quelque chose comme ceci :
from flask import Flask
from your_flask_app_file import app  # replace with your filename

class TestFlaskRoutes(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        
    def test_index_route(self):
        response = self.client.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_route(self):
        response = self.client.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
if __name__ == '__main__':
    unittest.main()
