"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from django.contrib.auth.models import User
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

        self.assertEquals(str(Item.objects.monthly_transaction(2010,3)),'[<Item: Heater>, <Item: Beans, butter, salmon>, <Item: washing liquid, hand wash, bin bag>, <Item: sweet>, <Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')

class ItemTest(TestCase):
    fixtures = ['test_data']

    def test_user_address(self):
        newitem = Item.objects.get(pk=1)
        self.assertEquals('116A,HA8 0BB', newitem.user_address(), "Address did not match")

class AddressTestCase(TestCase):
    fixtures = ['test_data']

    def test_monthly_avg(self):
        """
        Test the monthly avg for this address
        """
        address = Address.objects.get(pk=1)
        self.failUnlessEqual(Decimal('9.8'), address.monthly_avg(2010, 3))

    def test_monthly_total(self):
        """
        Test Monthly total for the specific address
        """
        address = Address.objects.get(pk=1)
        self.failUnlessEqual(Decimal('19.55'), address.monthly_total(2010, 3))
    
    def test_monthly_transaction(self):
        """
        Test Monthly transaction for specific address
        """
        address = Address.objects.get(pk=1)
        self.failUnlessEqual(str(address.monthly_transaction(2010,3)),'[<Item: washing liquid, hand wash, bin bag>, <Item: sweet>, <Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')

    def test_category_summary(self):
        """
        Test Monthly Category summery for an address
        """
        address = Address.objects.get(pk=1)
        summary = dict((c.name, c.item__price__sum) for c in address.category_summary(2010, 3))
        self.failUnlessEqual(summary, {u'Grocery': Decimal('14.88'), u'HouseHold': Decimal('4.67')})

    def test_category_transaction(self):
        """
        Test monthly transaction by category
        """
        address = Address.objects.get(pk=1)
        self.failUnlessEqual(str(address.category_transaction('Grocery',2010,3)),'[<Item: sweet>, <Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')

 
class ProfileTestCase(TestCase):
    fixtures = ['test_data']
    
    def test_monthly_usr(self):
        """
        Test how many user is living for this month for that address
        """
        rocky = User.objects.get(username__exact='rocky')
        self.failUnlessEqual(Decimal('9.88'), rocky.profile.monthly_total(2010, 3))
    
    def test_monthly_transaction(self):
        """
        Test monthly user transaction for individual user
        """
        user = User.objects.get(username__exact='rocky')
        self.failUnlessEqual(str(user.profile.monthly_transaction(2010,3)), '[<Item: Eggs>, <Item: tea, suger, milk, eve milk, mayo>]')

    def test_is_housemate_of(self):
        rocky = User.objects.get(username='rocky')
        anu = User.objects.get(username='anu')
        roman = User.objects.get(username='roman')
        self.assertTrue(anu.profile.is_housemate_of(rocky))
        self.assertTrue(rocky.profile.is_housemate_of(anu))
        self.assertFalse(rocky.profile.is_housemate_of(roman))

    def test_left_housemates(self):
        rocky = User.objects.get(username='rocky')
        sumon = User.objects.get(username='sumon')
        self.assertFalse(rocky.profile.is_housemate_of(sumon))
    
    def test_has_address(self):
        rocky = User.objects.get(username='rocky')
        self.assertTrue(rocky.profile.has_address())
    
#    def test_was_invited(self):
#        rocky = User.objects.get(username='rocky')
#        sumon = User.objects.get(username='sumon')
#        self.assertFalse(rocky.profile.was_invited())
#        self.assertTrue(sumon.profile.was_invited())

#    def test_from_user_address(self):
#        sumon = User.objects.get(username='sumon')
#        self.failUnlessEqual(str(sumon.profile.from_user_address()), '116A')

    def test_get_user(self):
        rocky = User.objects.get(username='rocky')
        self.assertTrue(rocky in rocky.profile.get_user(), \
                    "user not found")

    def test_get_housemates(self):
        rocky = User.objects.get(username='rocky')
        anu = User.objects.get(username='anu')
        self.assertTrue(anu in rocky.profile.get_housemates(), \
                    "housemates not found")
    
