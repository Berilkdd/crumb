from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("gate/", views.checkout_gate, name="checkout_gate"),
]