from django.urls import reverse_lazy
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AdminAuthForm
from .mixins import AdminTemplateView, AdminView


class AdminSingInView(LoginView):
    authentication_form = AdminAuthForm
    template_name = "admin/sign_in.html"
    redirect_authenticated_user=True

    def form_valid(self, form):
        user = form.get_user()
        if user.is_admin is True:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(reverse_lazy("admin_sign_in"))        


class AdminSingOutView(AdminView, LogoutView):
    template_name = "admin/sign_out.html"


class AdminIndexView(AdminTemplateView):
    admin_required = True
    template_name = "admin/index.html"
