from django.test import TestCase
from django.contrib.auth.models import Group, User, Permission

class FlatAdminGroupTest(TestCase):
	fixtures = ['test_data']

	def setUp(self):
		self.g = Group.objects.filter(name='Flat Admin')[0]
		self.g.permissions.add(Permission.objects.filter(name="Can add item")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can change item")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can delete item")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can add category")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can change category")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can delete category")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can change profile")[0])
		self.g.permissions.add(Permission.objects.filter(name="Can change address")[0])
		self.u = User.objects.get(username='rocky') 

	def test_group_exists(self):
		self.failUnlessEqual(str(self.g), str('Flat Admin'), \
				"The Flat Admin Group does not exist")
	
	def test_user_is_flat_admin(self):
		self.failUnlessEqual(self.u.is_staff, True, "User is not flat admin")
	
	def test_user_has_group(self):
		self.failUnlessEqual(str(self.u.groups.filter(name='Flat Admin')[0]), \
				str('Flat Admin'), "User does not belong to this group")

	def test_user_group_permissions(self):
		self.failUnlessEqual(self.u.has_perm(u'core.add_address'), False)
		self.failUnlessEqual(self.u.has_perm(u'core.delete_address'), False)
		self.failUnlessEqual(self.u.has_perm(u'core.add_profile'), False)
		self.failUnlessEqual(self.u.has_perm(u'core.delete_profile'), False)
		self.failUnlessEqual(self.u.has_perm(u'core.add_category'), True)
		self.failUnlessEqual(self.u.has_perm(u'core.delete_category'), True)
		self.failUnlessEqual(self.u.has_perm(u'core.add_item'), True)
		self.failUnlessEqual(self.u.has_perm(u'core.delete_item'), True)
		self.failUnlessEqual(self.u.has_perm(u'core.change_profile'), True)
