from django.contrib import admin

from iflatshare.core.models import Address, Item, Category, Profile

class ItemAdmin(admin.ModelAdmin):
	date_hierarchy = 'purchase_date'
	list_display = ('name', 'price', 'user', 'purchase_date', 'category', \
	                'user_address')
	ordering = ('-purchase_date',)

	def queryset(self, request):
		qs = super(ItemAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(user__profile__address=request.user.profile.address)

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		if not request.user.is_superuser:
			if db_field.name == 'user':
				kwargs['queryset'] = request.user.profile.get_housemates()
			if db_field.name == 'category':
				kwargs['queryset'] = request.user.profile.address.categories.all()
			return super(ItemAdmin, self).formfield_for_foreignkey(db_field,\
		                                                    request, **kwargs)
		return super(ItemAdmin, self).formfield_for_foreignkey(db_field,\
		                                                    request, **kwargs)

class AddressAdmin(admin.ModelAdmin):
	list_display = ('house_number', 'post_code', 'street_name', 'city', \
	                'country')

	def queryset(self, request):
		qs = super(AddressAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(id=request.user.profile.address.id)

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','address','status','is_admin')
	list_editable = ('status','is_admin')
	ordering = ('-status',)
	readonly_fields = ('user','address')
	def queryset(self, request):
		qs = super(ProfileAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(address=request.user.profile.address)

admin.site.register(Address, AddressAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Profile, ProfileAdmin)