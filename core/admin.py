from iflatshare.core.models import Address, Item, Category, Profile
from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'purchase_date'
    list_display = ('name','price','user','purchase_date','category', 'user_address')    

admin.site.register(Address)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Profile)
