from django.urls import include, re_path

from keypair.views import KeyPairListAPI, KeyPairDataAPI

urlpatterns = [
    re_path(r"$", KeyPairListAPI.as_view(), name="keypair_list_api"),
    re_path(r"(?P<pk>\d+)/?$", KeyPairDataAPI.as_view(), name="keypair_data_api"),
]
