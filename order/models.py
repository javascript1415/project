from django.db import models
from product.models import Product , CartItem
from account.models import User

class Addres(models.Model):
    user  =  models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.IntegerField()
    city = models.CharField(max_length=250)
    muncipality = models.CharField(max_length=200)
    tol = models.CharField(max_length=100)
    landmark = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return f" {self.city}-{self.muncipality}-{self.tol}-{self.landmark}"
    

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orderasuser')
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orderasseller',default=None)
    items = models.ForeignKey(Product,on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'),('Cancelled','Cancelled')],
        default='Pending'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0.00)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user} - {self.items}"
    