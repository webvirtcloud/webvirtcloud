from django.urls import re_path
from .views import AdminImageIndexView, AdminImageCreateView, AdminImageUpdateView, AdminImageDeleteView


urlpatterns = [
    re_path("$", AdminImageIndexView.as_view(), name="admin_image_index"),
    re_path("create/?$", AdminImageCreateView.as_view(), name="admin_image_create"),
    re_path("update/(?P<pk>\d+)/?$", AdminImageUpdateView.as_view(), name="admin_image_update"),
    re_path("delete/(?P<pk>\d+)/?$", AdminImageDeleteView.as_view(), name="admin_image_delete"),
]
