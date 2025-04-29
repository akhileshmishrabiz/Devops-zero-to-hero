import unittest
from app import app  # assuming your Flask app is named app.py and has an app object
import logging

logging.basicConfig(level=logging.INFO)

class FlaskTest(unittest.TestCase):
    
    # Ensure that Flask was set up correctly
    def test_index(self):
        logging.info("TEST-01: Checking if Flask is Setup...")
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    # Ensure that the main page loads correctly
    def test_index_loads(self):
        logging.info("TEST-02: Checking if the main page loads...")
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'Welcome' in response.data)
    
    # Ensure that products endpoint behaves correctly
    def test_products_endpoint(self):
        logging.info("TEST-03: Checking if the products endpoint is working...")
        tester = app.test_client(self)
        response = tester.get('/api/products', content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    # Ensure products endpoint data is correct
    def test_products_data(self):
        logging.info("TEST-04: Checking for product data sanity...")
        tester = app.test_client(self)
        response = tester.get('/api/products', content_type='application/json')
        self.assertTrue(b'name' in response.data)
        self.assertTrue(b'image_url' in response.data)

if __name__ == '__main__':
    unittest.main()
