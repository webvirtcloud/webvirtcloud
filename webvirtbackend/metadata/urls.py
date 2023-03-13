from django.urls import include, re_path

from .v1.views import MetadataV1Json

urlpatterns = [
    re_path(r"v1.json", MetadataV1Json.as_view(), name="metadata_json"),
    re_path(r"v1/?", include("metadata.v1.urls")),
]
