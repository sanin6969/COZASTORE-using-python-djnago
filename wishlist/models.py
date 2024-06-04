from django.db import models
from store.models import Product
from accounts.models import Account
# Create your models here.
class Wishlist(models.Model):
    wish_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField( auto_now_add=True)
    
    def __str__(self):
        return self.wish_id
    
class WishItem(models.Model):
    user= models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    # variation=models.ManyToManyField(Variation,blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)    
    wish=models.ForeignKey(Wishlist,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()    
    is_active=models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.product_price* self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product}"