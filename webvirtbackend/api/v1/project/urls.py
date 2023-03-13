from django.urls import include, re_path

from project.views import ProjectDefaultAPI, ProjectListAPI, ProjectDataAPI

urlpatterns = [
    re_path(r"default/?$", ProjectDefaultAPI.as_view(), name="project_default_api"),
    re_path(r"$", ProjectListAPI.as_view(), name="project_list_api"),
    re_path(r"(?P<uuid>[0-9a-f-]+)/?$", ProjectDataAPI.as_view(), name="project_data_api"),
]
