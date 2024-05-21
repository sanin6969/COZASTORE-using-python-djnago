from django.contrib import admin
from . import models
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_price','product_stock','category','is_available')
    prepopulated_fields={'product_slug':('product_name',)}
    
admin.site.register(models.Product,ProductAdmin)
# admin.site.register(models.Variation)
