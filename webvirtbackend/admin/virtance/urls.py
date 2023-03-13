from django.urls import re_path
from .views import AdminVirtanceIndexView


urlpatterns = [
    re_path("$", AdminVirtanceIndexView.as_view(), name="admin_virtance_index"),
]
