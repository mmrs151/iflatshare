from django.db import models
from invitation.models import InvitationKey
from django.contrib.auth.models import User as AuthUser
from django.db.models import Sum
from decimal import *
from django.db.models.signals import post_save
from iflatshare.core import signals as custom_signals


class Address(models.Model):
    house_number = models.CharField(max_length=200)
    post_code = models.CharField(max_length=8)
    street_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __unicode__(self):
        return self.house_number

    class Meta:
        unique_together = (("house_number", "post_code"))
    
    def monthly_avg(self, year, month):
        try:
            getcontext().prec = 2
            total_user = AuthUser.objects.filter(profile__address=self).count()
            monthly_avg = Decimal(self.monthly_total(year, month)/total_user)
        except TypeError:
            monthly_avg =0
        return monthly_avg

    def monthly_total(self, year, month):
        queryset = Item.objects.monthly_transaction(year, month).filter(user__profile__address=self.pk)
        if not queryset:
            return 0
        return queryset.aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return Item.objects.monthly_transaction(year, month).filter(user__profile__address=self)

    def category_summary(self, year, month):
        return Category.objects.filter(item__purchase_date__year=year, item__purchase_date__month=month, item__user__profile__address=self).annotate(Sum('item__price'))
    
    def category_transaction(self,category, year, month):
        return self.monthly_transaction(year, month).filter(category__name=category)

class ProfileManager(models.Manager):
    def create_from_user(self, user):
        self.create(user=user)

class Profile(models.Model):
    user = models.OneToOneField(AuthUser)
    address = models.ForeignKey(Address, blank=True, null=True)
    CHOICES = (
        ('present', 'Present'),
        ('left', 'Left'),
    )
    status = models.CharField(max_length=7, choices=CHOICES)

    objects = ProfileManager()
    
    def __unicode__(self):
        return u'%s, %s' % (unicode(self.user), unicode(self.address))
    
    def get_housemates(self):
        return AuthUser.objects.filter(profile__address=self.address)

    def monthly_total(self, year, month):
        queryset = self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month).aggregate(Sum('price'))['price__sum']
        if queryset is None:
            return 0
        return queryset

    def monthly_transaction(self, year, month):
        return self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month)

    def is_housemate_of(self, other_user):
        return self.address == other_user.profile.address

    def has_address(self):
        return self.address is not None

    def was_invited(self):
        try:
            invited = InvitationKey.objects.get(registrant=self.user)
            return True
        except InvitationKey.DoesNotExist:
            return False

    def from_user_address(self):
        key = InvitationKey.objects.get(registrant=self.user)
        return key.from_user.profile.address
    
post_save.connect(custom_signals.assign_address, sender=Profile)

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class ItemManager(models.Manager):
    def monthly_total(self, year, month):
        return self.monthly_transaction(year, month).aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return self.get_query_set().filter(purchase_date__year=year, purchase_date__month=month)

class Item(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(AuthUser)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    purchase_date = models.DateField(auto_now=True)

    objects = ItemManager()

    def __unicode__(self):
        return self.name
