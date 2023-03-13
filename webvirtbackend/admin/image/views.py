from django import forms
from django.urls import reverse_lazy
from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineCheckboxes
from .forms import FormImage, CustomModelMultipleChoiceField
from image.models import Image
from region.models import Region
from admin.mixins import AdminTemplateView, AdminFormView, AdminUpdateView, AdminDeleteView, AdminTemplateView


class AdminImageIndexView(AdminTemplateView):
    template_name = 'admin/image/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(is_deleted=False)
        return context


class AdminImageCreateView(AdminFormView):
    template_name = 'admin/image/create.html'
    form_class = FormImage
    success_url = reverse_lazy('admin_image_index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AdminImageUpdateView(AdminUpdateView):
    template_name = 'admin/image/update.html'
    template_name_suffix = "_form"
    model = Image
    success_url = reverse_lazy('admin_image_index')
    fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminImageUpdateView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "name", "slug", "type", "description", "md5sum", "distribution", "file_name",
            InlineCheckboxes("regions", css_class="checkboxinput"),
            "is_active"
        )
            
    def get_form(self, form_class=None):
        form = super(AdminImageUpdateView, self).get_form(form_class)
        form.fields["regions"] = CustomModelMultipleChoiceField(
            queryset=Region.objects.filter(is_deleted=False), 
            widget=forms.CheckboxSelectMultiple()
        )
        return form
    
    def get_context_data(self, **kwargs):
        context = super(AdminImageUpdateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context


class AdminImageDeleteView(AdminDeleteView):
    template_name = 'admin/image/delete.html'
    model = Image
    success_url = reverse_lazy('admin_image_index')

    def delete(self, request, *args, **kwargs):
        image = self.get_object()
        image.delete()
        return super(self).delete(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AdminImageDeleteView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def get_context_data(self, **kwargs):
        context = super(AdminImageDeleteView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context
