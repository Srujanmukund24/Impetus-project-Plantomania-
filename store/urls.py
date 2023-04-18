from django.urls import path,include
from . import views
urlpatterns = [
    path('store/', views.store, name="store"),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cartview/', views.cart, name='cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('plantoptions/', views.plantop, name='plantop'),
    path('checkout/', views.checkout, name='checkout'),
    path('createp/', views.create_payment, name='createp'),
    path('checkout/success', views.sucess, name='sucess'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

]
