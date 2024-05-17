from django.urls import path
from .views import details,shop

urlpatterns = [
    path('shop',shop, name='shop'),
    path('<slug:category_slug>/',shop, name='product_by_category'),
    path('details',details, name='details'),
    path('<slug:category_slug>/<slug:product_slug>/',details, name='product_detail'),
    
]