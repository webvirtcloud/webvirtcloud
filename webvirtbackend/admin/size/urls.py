from django.urls import re_path
from .views import AdminSizeIndexView, AdminSizeCreateView, AdminSizeUpdateView, AdminSizeDeleteView


urlpatterns = [
    re_path("$", AdminSizeIndexView.as_view(), name="admin_size_index"),
    re_path("create/?$", AdminSizeCreateView.as_view(), name="admin_size_create"),
    re_path("update/(?P<pk>\d+)/?$", AdminSizeUpdateView.as_view(), name="admin_size_update"),
    re_path("delete/(?P<pk>\d+)/?$", AdminSizeDeleteView.as_view(), name="admin_size_delete"),
]
