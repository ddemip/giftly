from django.contrib import admin
from django.urls import path
import giftlyapp.views as views

urlpatterns = [
    # Home view
    path('', views.home, name='home'),
    # All Products view
    path('products/', views.all_products, name='all_products'),
    # Product Detail view
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    path('admin/', admin.site.urls),
]
