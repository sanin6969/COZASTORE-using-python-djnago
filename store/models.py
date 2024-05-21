from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

variation_category_choice=(
    ('color','color'),
    ('size','size')
)
class Product(models.Model):
    product_name=models.CharField(max_length=150,unique=True)
    product_brand=models.CharField(max_length=50,default=None)
    product_slug=models.SlugField(max_length=150,unique=True)
    product_description=models.TextField(max_length=500)
    product_price=models.IntegerField()
    product_image=models.ImageField(upload_to='photos/products')
    product_stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    # product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice,default=True)
    variation_value=models.CharField(max_length=100,default=True)
    is_active=models.BooleanField(default=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.product_slug])
    def __str__(self):
        return self.product_name
    

# class Variation(models.Model):
    
    # def __str__(self):
    #     return self.product
    
    
    