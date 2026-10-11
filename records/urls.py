from django.urls import path
from . import views

urlpatterns = [
    path("", views.records, name="records"),
    path("<int:record_id>/", views.record_detail, name="record_detail"),
]
