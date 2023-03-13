from django.urls import re_path
from .views import AdminNetworkIndexView, AdminNetworkCreateView, AdminNetworkUpdateView, AdminNetworkDeleteView


urlpatterns = [
    re_path("$", AdminNetworkIndexView.as_view(), name="admin_network_index"),
    re_path("create/?$", AdminNetworkCreateView.as_view(), name="admin_network_create"),
    re_path("update/(?P<pk>\d+)/?$", AdminNetworkUpdateView.as_view(), name="admin_network_update"),
    re_path("delete/(?P<pk>\d+)/?$", AdminNetworkDeleteView.as_view(), name="admin_network_delete"),
]
