from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from .forms import FormNetwork
from network.models import Network
from admin.mixins import AdminTemplateView, AdminFormView, AdminUpdateView, AdminDeleteView


class AdminNetworkIndexView(AdminTemplateView):
    template_name = 'admin/network/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['networks'] = Network.objects.filter(is_deleted=False)
        return context


class AdminNetworkCreateView(AdminFormView):
    template_name = 'admin/network/create.html'
    form_class = FormNetwork
    success_url = reverse_lazy('admin_network_index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AdminNetworkUpdateView(AdminUpdateView):
    template_name = 'admin/network/update.html'
    template_name_suffix = "_form"
    model = Network
    success_url = reverse_lazy('admin_network_index')
    fields = ["cidr", "netmask", "dns1", "dns2", "is_active"]

    def __init__(self, *args, **kwargs):
        super(AdminNetworkUpdateView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(AdminNetworkUpdateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context


class AdminNetworkDeleteView(AdminDeleteView):
    template_name = 'admin/network/delete.html'
    model = Network
    success_url = reverse_lazy('admin_network_index')

    def delete(self, request, *args, **kwargs):
        region = self.get_object()
        region.delete()
        return super(self).delete(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AdminNetworkDeleteView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(AdminNetworkDeleteView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context
