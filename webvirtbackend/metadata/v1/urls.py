from django.urls import include, re_path

from .views import MetadataIndex


urlpatterns = [
    re_path(r"$", MetadataIndex.as_view(), name="metadata"),
]
