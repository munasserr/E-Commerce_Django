from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.shop , name = 'shop'),
    path('<int:id>', views.shopdet , name = 'shopdet'),
    path('cart/', views.cart , name = 'cart'),
    path('checkout/', views.checkout , name = 'checkout'),
    path('add_to_cart/<int:id>/', views.add_to_cart , name = 'add_to_cart'),
    path('add_coupon/', views.add_coupon , name = 'add_coupon'),
    path('remove_from_cart/<int:id>/', views.remove_from_cart , name = 'remove_from_cart'),
]