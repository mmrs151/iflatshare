from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models import Sum
from decimal import Decimal

class Address(models.Model):
    house_number = models.CharField(max_length=200)
    post_code = models.CharField(max_length=8)
    street_name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    passcode = models.CharField(max_length=8)

    def __unicode__(self):
        return self.house_number

    class Meta:
        unique_together = (("house_number", "post_code"))
    
    def monthly_avg(self, year, month):
        total_user = AuthUser.objects.filter(profile__address=self).count()
        monthly_avg = Decimal(self.monthly_total(year, month)/total_user)
        return monthly_avg

    def monthly_total(self, year, month):
        return Item.objects.monthly_transaction(year, month).filter(user__profile__address=self.pk).\
                aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return Item.objects.monthly_transaction(year, month).filter(user__profile__address=self)

    def category_summary(self, year, month):
        return Category.objects.filter(item__purchase_date__year=year, item__purchase_date__month=month, item__user__profile__address=self).annotate(Sum('item__price'))
    
    def category_transaction(self,category, year, month):
        return self.monthly_transaction(year, month).filter(category__name=category)

class Profile(models.Model):
    user = models.OneToOneField(AuthUser)
    address = models.ForeignKey(Address)
    
    def __unicode__(self):
        return u'%s, %s' % (unicode(self.user), unicode(self.address))
    
    def get_housemates(self):
        return AuthUser.objects.filter(profile__address=self.address)

    def monthly_total(self, year, month):
        return self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month).aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month)

    def is_housemate_of(self, other_user):
        return self.address == other_user.profile.address

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
