from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models import Sum

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

class User(AuthUser):
    address = models.ForeignKey(Address)

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class ItemManager(models.Manager):
    def monthly_total(self, month):
#        return self.get_query_set().aggregate(Sum('price'))
        return self.get_query_set().filter(date__month=month).aggregate(Sum('price'))['price__sum']

class Item(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now=True)

    objects = ItemManager()

    def __unicode__(self):
        return self.name