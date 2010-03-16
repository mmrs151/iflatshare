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
        total_user = self.user_set.count()
        monthly_avg = Decimal(self.monthly_total(year, month)/total_user)
        return monthly_avg

    def monthly_total(self, year, month):
        return Item.objects.monthly_transaction(year, month).filter(user__address=self).\
                aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return Item.objects.monthly_transaction(year, month).filter(user__address=self)

    def category_summery(self, year, month):
        return Category.objects.filter(item__purchase_date__year=year, item__purchase_date__month=month, item__user__address=self).annotate(Sum('item__price'))
    
    def category_transaction(self,category, year, month):
        return self.monthly_transaction(year, month).filter(category__name=category)

class UserManager(models.Manager):
    def get_from_auth_user(self, user):
        return self.get_query_set().get(pk=user.pk)

class User(AuthUser):
    address = models.ForeignKey(Address)

    objects = UserManager()
    
    def get_housemates(self):
        return self.address.user_set.all()

    def monthly_total(self, year, month):
        return self.item_set.filter(purchase_date__year=year, purchase_date__month=month).aggregate(Sum('price'))['price__sum']

    def monthly_transaction(self, year, month):
        return self.item_set.filter(purchase_date__year=year, purchase_date__month=month)

    def is_housemate_of(self, other_user):
        assert(isinstance(other_user, User))
        return self in other_user.get_housemates()

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
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    purchase_date = models.DateField(auto_now=True)

    objects = ItemManager()

    def __unicode__(self):
        return self.name
