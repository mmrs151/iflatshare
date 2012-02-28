from django.test import TestCase
from django.test.client import Client
from django.utils import unittest

class ViewTest(TestCase):
    fixtures = ['test_data']

    def setUp(self):
        self.c = Client()

    def test_index(self):
        """
        Test response for admin user
        """
        # check if admin view exist
        response = self.c.post('/admin/')
        self.assertEqual(response.status_code, 200)

        # check if admin can login successfully
        self.assertEqual(self.c.login(username='testadmin', password='mm'), True)
        
        # check if any other view get redirects apart form admin
        response = self.c.get('/')
        self.assertEqual(response.status_code, 302)

        response = self.c.get('/item/')
        self.assertEqual(response.status_code, 302)

        response = self.c.get('/avg_diff/')
        self.assertEqual(response.status_code, 302)        
