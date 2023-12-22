from django.contrib import admin
from django.urls import path
from . import views
from .views import upload_product, product_list, view_cart, add_to_cart, purchase_cart
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.base, name='base'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.user_home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('product/', views.product, name='product'),
    path('upload/', views.upload_product, name='upload_product'),
    path('product_list/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('purchase_cart/', views.purchase_cart, name='purchase_cart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)