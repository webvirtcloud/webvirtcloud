from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin:
    admin_required = False

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_active:
                return redirect(reverse_lazy("admin_sign_out"))

        if self.admin_required:
            if not request.user.is_admin:
                messages.error(request, "You don't have permission to access this page.")
                return redirect(reverse_lazy("admin_sign_out"))

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminView(LoginRequiredMixin, View):
    pass

class AdminFormView(LoginRequiredMixin, FormView):
    pass

class AdminUpdateView(LoginRequiredMixin, UpdateView):
    pass

class AdminDeleteView(LoginRequiredMixin, DeleteView):
    pass

class AdminTemplateView(LoginRequiredMixin, TemplateView):
    pass
