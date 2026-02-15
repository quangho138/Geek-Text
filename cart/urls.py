from django.urls import path
from . import views

urlpatterns=[
    path('cart/',views.get_cart, name='get_cart'),
]