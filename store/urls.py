from django.urls import path,include
from . import views
urlpatterns = [
    path('store/', views.store, name="store"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cartview/', views.cart, name='cart'),
    path('update_cart', views.update_cart, name='update_cart'),
]
