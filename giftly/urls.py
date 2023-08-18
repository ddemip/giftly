from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import giftlyapp.views as views
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.all_products, name='all_products'),
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('cart/', views.cart_view, name='cart'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
