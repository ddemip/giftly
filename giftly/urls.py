from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import giftlyapp.views as views
from django.contrib.staticfiles.urls import static
from django.conf import settings
from weather_widget import views as weather_views

urlpatterns = [
    path('', views.home, name='home'),
    path('check_orders/', views.check_orders, name='check_orders'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('search/', views.search_products, name='search_products'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('weather_widget/fetch_weather/', weather_views.fetch_weather, name='fetch_weather'),
    path('products/', views.all_products, name='all_products'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login_1'),
    path('profile/', views.user_profile_view, name='profile'),
    path('profile/<int:pk>/', views.user_profile_view, name='profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('password_change/', views.password_change, name='pwd-reset'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('<slug:category_slug>/', views.all_products, name='category_products'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail_view, name='product_detail_by_category'),
    path('product/<slug:product_slug>/', views.product_detail_view, name='product_detail_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
