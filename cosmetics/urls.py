from django.urls import path
from . import views

urlpatterns = [
    path("", views.cosmetics, name="cosmetics"),
    path("<int:cosmetic_id>/", views.cosmetic_detail, name="cosmetic_detail"),
]
