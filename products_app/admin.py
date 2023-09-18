from django.contrib import admin

from products_app.views import cart
from .models import *
# Register your models here.
admin.site.register(product)
admin.site.register(productimage)
admin.site.register(category)
admin.site.register(product_alternative)
admin.site.register(product_accessory)
admin.site.register(cart) 
admin.site.register(order)
admin.site.register(orderItem)
admin.site.register(ShppingAdress)
admin.site.register(custommer)

