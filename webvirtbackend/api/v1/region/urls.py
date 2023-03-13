from django.urls import include, re_path

from region.views import RegionListAPI

urlpatterns = [
    re_path(r"$", RegionListAPI.as_view(), name="region_list_api"),
]
