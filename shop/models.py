from django.db import models
import datetime
import os
from django.contrib.auth.models import User

# Create your models here.

def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y:m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time, filename)
    return os.path.join("uploads/", new_filename)


class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False )
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    vendor = models.CharField(max_length=200, null=False, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)    


    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    products=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False, blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)    


    @property
    def total_costs(self):
        return self.product_qty * self.products.selling_price
    

class Favourite(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    products=models.ForeignKey(Product, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)     