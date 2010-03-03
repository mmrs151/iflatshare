from django.db import models
from django.contrib.auth.models import User as AuthUser


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

class Item(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.name
