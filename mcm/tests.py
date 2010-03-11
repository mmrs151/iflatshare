"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from decimal import Decimal

class ItemManagerTest(TestCase):
    fixtures = ['test_data']

    def test_monthly_total(self):
        """
        Tests the monthly total method of ItemManager
        """
        self.failUnlessEqual(Decimal('68.89'), Item.objects.monthly_total(2010, 3))

    def test_monthly_transaction(self):
        """
        Test the montyly transaction list
        """

        self.assertEquals(str(Item.objects.monthly_transaction(2010,3)),'[<Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>, <Item: washing liquid, hand wash, bin bag>, <Item: sweet>, <Item: Heater>, <Item: Beans, butter, salmon>]')

class AddressTestCase(TestCase):
    fixtures = ['test_data']

    def test_monthly_avg(self):
        """
        Test the monthly avg for this address
        """
        address = Address.objects.all()[0]
        self.failUnlessEqual(Decimal('9.775'), address.monthly_avg(2010, 3))

    def test_monthly_total(self):
        """
        Test Monthly total for the specific address
        """
        address = Address.objects.all()[0]
        self.failUnlessEqual(Decimal('19.55'), address.monthly_total(2010, 3))
    
    def test_monthly_transaction(self):
        """
        Test Monthly transaction for specific address
        """
        address = Address.objects.all()[0]
        self.failUnlessEqual(str(address.monthly_transaction(2010,3)),'[<Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>, <Item: washing liquid, hand wash, bin bag>, <Item: sweet>]')

class UserTestCase(TestCase):
    fixtures = ['test_data']
    
    def test_monthly_usr(self):
        """
        Test how many user is living for this month for that address
        """
        rocky = User.objects.get(username__exact='rocky')
        self.failUnlessEqual(Decimal('9.88'), rocky.monthly_total(2010, 3))
    
    def test_monthly_transaction(self):
        """
        Test monthly user transaction for individual user
        """
        user = User.objects.get(username__exact='rocky')
        self.failUnlessEqual(str(user.monthly_transaction(2010,3)), '[<Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')
