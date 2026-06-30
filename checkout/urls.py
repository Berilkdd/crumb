from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("gate/", views.checkout_gate, name="checkout_gate"),
    path("success/<int:order_id>/", views.checkout_success, name="checkout_success",),
    path("wh/", views.webhook, name="webhook"),
]