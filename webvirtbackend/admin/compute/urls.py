from django.urls import re_path
from .views import AdminComputeIndexView, AdminComputeCreateView, AdminComputeUpdateView, AdminComputeDeleteView
from .views import AdminComputeOverviewView
from .views import AdminComputeStoragesView, AdminComputeStorageView
from .views import AdminComputeNetworksView, AdminComputeNetworkView
from .views import AdminComputeSecretsView
from .views import AdminComputeNwfiltersView


urlpatterns = [
    re_path("$", AdminComputeIndexView.as_view(), name="admin_compute_index"),
    re_path("create/?$", AdminComputeCreateView.as_view(), name="admin_compute_create"),
    re_path("update/(?P<pk>\d+)/?$", AdminComputeUpdateView.as_view(), name="admin_compute_update"),
    re_path("delete/(?P<pk>\d+)/?$", AdminComputeDeleteView.as_view(), name="admin_compute_delete"),

    re_path("(?P<pk>\d+)/overview/?$", AdminComputeOverviewView.as_view(), name="admin_compute_overview"),
    re_path("(?P<pk>\d+)/storages/?$", AdminComputeStoragesView.as_view(), name="admin_compute_storages"),
    re_path(
        "(?P<pk>\d+)/storages/(?P<pool>[\w\d\-]+)/?$", AdminComputeStorageView.as_view(), name="admin_compute_storage"
    ),
    re_path("(?P<pk>\d+)/networks/?$", AdminComputeNetworksView.as_view(), name="admin_compute_networks"),
    re_path(
        "(?P<pk>\d+)/networks/(?P<pool>[\w\d\-]+)/?$", AdminComputeNetworkView.as_view(), name="admin_compute_network"
    ),
    re_path("(?P<pk>\d+)/secrets/?$", AdminComputeSecretsView.as_view(), name="admin_compute_secrets"),
    re_path("(?P<pk>\d+)/nwfilters/?$", AdminComputeNwfiltersView.as_view(), name="admin_compute_nwfilters"),
]
