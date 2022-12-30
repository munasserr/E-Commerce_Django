    
from decimal import Decimal


from django.db import models
from django.conf import settings
from home_app.models import *
from django_countries.fields import CountryField
# Create your models here.



class Coupon(models.Model):
    code = models.CharField(max_length = 16)
    amount = models.FloatField(null=False , default=10)
    def __str__(self):
        return self.code

class CartItem(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , null = True ,blank=True)
    ordered = models.BooleanField(default =  False)
    item = models.ForeignKey(Product , on_delete = models.CASCADE,null=True)
    quantity = models.IntegerField(default=1 , null = True)

    def __str__(self) :
        return f" {self.quantity} of ({self.item})"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discounted_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        
        return self.get_total_item_price()

#-------------------------------------
class Cart(models.Model) :
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , null = True, blank=True)
    items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add = True , null = True)
    orderd_date = models.DateTimeField(null = True ,blank=True)
    ordered = models.BooleanField(default =  False)
    coupon = models.ForeignKey(Coupon, blank=True ,  on_delete = models.SET_NULL ,  null=True)


    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        total = total - Decimal(self.coupon.amount)+ 2
        return total

    def get_sub_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_sub_total_without_coupon(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price() +2
        return total

    # def get_amount_saved(self):
    #     return self.items.get_total_item_price() - self.items.get_total_discount_item_price()

#-----------------------------------------------------

PAYMENT_CHOICES = (
    ('CD' , 'Credit Card'),
    ('DD' , 'Debit Card')
)


class Order(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , null = True, blank=True)
    cart = models.ForeignKey(Cart , blank=False ,  on_delete = models.SET_NULL ,  null=True)
    fname = models.CharField(null=True , blank=False, max_length=25)
    lname = models.CharField(null=True , blank=False , max_length=25)
    user_name = models.CharField(null=True , blank=False , max_length=25)
    email = models.EmailField(null=True)
    address = models.CharField(null=True , max_length=225)
    # address2 = models.CharField(null=False , max_length=225)
    country = CountryField(blank_label = '(select country)',null=True)
    zip = models.IntegerField(null=True , blank=False)
    payment_option = models.CharField(null=True ,choices=PAYMENT_CHOICES  , max_length=45 , default=None)
    # name_on_card = models.CharField(null=False , max_length=225)
    credit_card_number = models.IntegerField(null=True , blank=False)
    exp_date = models.DateField(null=True , blank=False)
    cvv = models.IntegerField(null=True , blank=False)
    ordered = models.BooleanField(default =  False)


