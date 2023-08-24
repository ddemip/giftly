from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import giftlyapp.views as views
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>/<slug:slug>', views.product_detail_view, name='product_detail'),
    path('products/', views.all_products, name='all_products'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login_1'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    path('products/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='pwd-reset'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # path('categories/', views.category_list, name='category_list'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/',
         views.cart_remove,
         name='cart_remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
