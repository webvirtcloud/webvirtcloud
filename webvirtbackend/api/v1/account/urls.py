from django.urls import include, re_path

from account.views import ProfileAPI, ChangePasswordAPI

urlpatterns = [
    re_path(r"profile/?$", ProfileAPI.as_view(), name="profile_api"),
    re_path(r"change_password/?$", ChangePasswordAPI.as_view(), name="change_password_api"),
]
