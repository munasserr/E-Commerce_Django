from django.contrib import admin
from .models import * 
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'name' , 'price' , 'img']

admin.site.register(Category)
admin.site.register(Product , ProductAdmin)
# Register your models here.
