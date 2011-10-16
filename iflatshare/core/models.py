from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.db.models import Sum
from decimal import *

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
            getcontext().prec = 4
            total_user = AuthUser.objects.filter(profile__address=self, profile__status='present').count()
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
    is_admin = models.BooleanField(default=False)

    objects = ProfileManager()
    
    def __unicode__(self):
        return u'%s, %s' % (unicode(self.user), unicode(self.address))

    def get_user(self):
        if self.status == 'present':
            return AuthUser.objects.filter(username=self.user)

    def get_housemates(self):
        if self.status == 'present':
            return AuthUser.objects.filter(profile__address=self.address, profile__status='present')

    def get_admin(self):
        if self.status == 'present':
            return AuthUser.objects.filter(profile__address=self.address, profile__is_admin=True)[0]

    def monthly_total(self, year, month):
        queryset = self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month).aggregate(Sum('price'))['price__sum']
        if queryset is None:
            return 0
        return queryset

    def monthly_transaction(self, year, month):
        return self.user.item_set.filter(purchase_date__year=year, purchase_date__month=month)

    def is_housemate_of(self, other_user):
        return self.address == other_user.profile.address and self.status == other_user.profile.status

    def has_address(self):
        try:
            return self.address is not None
        except DoesNotExist:
            raise Exception('Profile has no address')    

    def send_activation_email(self, site):
        ctx_dict = { 'activation_key': self.activation_key,
                     'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                     'site': site }
        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('registration/activation_email.txt',
                                   ctx_dict)
        
        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

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
    price = models.DecimalField(max_digits=7, decimal_places=2)
    purchase_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-purchase_date']

    objects = ItemManager()

    def __unicode__(self):
        return self.name

    def user_address(self):
        address = self.user.profile.address.house_number + "," \
                + self.user.profile.address.post_code
        return address
