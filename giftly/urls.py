from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import giftlyapp.views as views
from django.contrib.staticfiles.urls import static
from django.conf import settings
from weather_widget import views as weather_views

urlpatterns = [
    path('', views.home, name='home'),
    path('weather_widget/fetch_weather/', weather_views.fetch_weather, name='fetch_weather'),
    path('products/', views.all_products, name='all_products'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login_1'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('password_change/', views.password_change, name='pwd-reset'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
    path('<slug:category_slug>/', views.all_products, name='category_products'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail_view, name='product_detail_by_category'),
    # path('categories/', views.category_list, name='category_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
