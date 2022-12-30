from django.db import models
from datetime import datetime


class Category(models.Model) :
    name = models.CharField(max_length=50 , null = True)
    def __str__(self) :
        return self.name

class Size(models.Model) :
    size_name = models.CharField(max_length = 5 , null=True)
    def __str__(self) :
        return self.size_name

class Product(models.Model):
    count = 0

    cat = [
        ('Shirt' , 'Shirt'),
        ('T-Shirt' , 'T-Shirt'),
        ('Pants' , 'Pants'),
        ('Watch' , 'Watch'),
        ('Bag' , 'Bag'),
    ]

    stts = [
        ('top-featured' , 'Top Featured' ),
        ('best-seller' , 'Best Seller'),
    ]

    typ= [
        ('Sale' , 'Sale'),
        ('New' , 'New'),
    ]

    name = models.CharField(max_length=45)
    price = models.DecimalField(null=True , max_digits=9 ,decimal_places=2 ,blank = True)
    discounted_price = models.DecimalField(null=True , max_digits=9 ,decimal_places=2 ,blank = True)
    img = models.ImageField(upload_to = 'photos' , null = True , blank = True)
    status = models.CharField(max_length=45, choices=stts ,null = True)
    category = models.ForeignKey(Category , on_delete=models.PROTECT ,null = True)
    type = models.CharField(max_length=45, choices=typ , null = True)
    data_added = models.DateField(default=datetime.now())
    quantity = models.IntegerField(null=True)
    size = models.ManyToManyField(Size)
    description = models.TextField(null=False , default = f"""The dress' waist is narrow, but it's a tight fit. A large belt helps accentuate her waist in a stylish manner.
Below the waist the dress widens and has multiple symmetric layers towards the bottom. The dress reaches to just below her knees and is slightly longer at the sides.
""")

    count += 1

    def __str__(self) :
        return self.name