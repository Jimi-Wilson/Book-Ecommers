from django.contrib import admin
from Inventory.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddressModel)
