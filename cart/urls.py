from django.urls import path
from . import views

urlpatterns=[
    path('cart/',views.get_cart, name='get_cart'),
    path('cart/subtotal/', views.get_subtotal, name='get_subtotal'), 
    path('cart/items/', views.add_to_cart, name='add_to_cart'),   
    path('cart/items/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/items/delete/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]