from django.contrib import admin

from shopping_app.models import *
from home_app.models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'user' , ]


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Size)
admin.site.register(Order , OrderAdmin)
admin.site.register(Coupon)
# Register your models here.
