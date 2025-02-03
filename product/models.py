from django.db import models
from account.models import User

class Product(models.Model):
    seller = models.ForeignKey(
        User,  # Reference to the User model
        on_delete=models.CASCADE,  # Delete products if the seller is deleted
        related_name='products'  # Allows reverse lookup (user.products.all())
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=100)

    def __str__(self):
        return self.name



class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sell = models.ForeignKey(User,on_delete=models.CASCADE,default = None,null=True,blank=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity