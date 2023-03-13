from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from .forms import FormRegion
from region.models import Region
from admin.mixins import AdminTemplateView, AdminFormView, AdminUpdateView, AdminDeleteView


class AdminRegionIndexView(AdminTemplateView):
    template_name = 'admin/region/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.filter(is_deleted=False)
        return context


class AdminRegionCreateView(AdminFormView):
    template_name = 'admin/region/create.html'
    form_class = FormRegion
    success_url = reverse_lazy('admin_region_index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AdminRegionUpdateView(AdminUpdateView):
    template_name = 'admin/region/update.html'
    template_name_suffix = "_form"
    model = Region
    success_url = reverse_lazy('admin_region_index')
    fields = ["name", "slug", "description", "is_active"]

    def __init__(self, *args, **kwargs):
        super(AdminRegionUpdateView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(AdminRegionUpdateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context


class AdminRegionDeleteView(AdminDeleteView):
    template_name = 'admin/region/delete.html'
    model = Region
    success_url = reverse_lazy('admin_region_index')

    def delete(self, request, *args, **kwargs):
        region = self.get_object()
        region.delete()
        return super(self).delete(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AdminRegionDeleteView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(AdminRegionDeleteView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context
