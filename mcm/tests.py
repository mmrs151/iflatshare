"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Item
from decimal import Decimal

class ItemManagerTest(TestCase):
    fixtures = ['test_data']

    def test_monthly_total(self):
        """
        Tests the monthly total method of ItemManager
        """
        self.failUnlessEqual(Decimal('9.88'), Item.objects.monthly_total(2010, 3))

    def test_monthly_transaction(self):
        """
        Test the montyly transaction list
        """

        self.assertEquals(str(Item.objects.monthly_transaction(2010,3)),'[<Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')
