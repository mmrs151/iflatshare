"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Item
from decimal import Decimal

class ItemManagerTest(TestCase):
    def test_monthly_total(self):
        """
        Tests the monthly total method of ItemManager
        """
        month = 3
        self.failUnlessEqual(Decimal('9.88'), Item.objects.monthly_total(month))
