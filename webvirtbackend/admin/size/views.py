from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineCheckboxes

from size.models import Size
from region.models import Region
from .forms import FormSize, CustomModelMultipleChoiceField
from admin.mixins import AdminTemplateView, AdminFormView, AdminUpdateView, AdminDeleteView


class AdminSizeIndexView(AdminTemplateView):
    template_name = 'admin/size/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sizes'] = Size.objects.filter(is_deleted=False)
        return context


class AdminSizeCreateView(AdminFormView):
    template_name = 'admin/size/create.html'
    form_class = FormSize
    success_url = reverse_lazy('admin_size_index')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # def get_form(self, form_class=None):
    #     form = super(AdminSizeCreateView, self).get_form(form_class)
    #     form.helper.exclude_by_widget(forms.CheckboxSelectMultiple())
    #     return form


class AdminSizeUpdateView(AdminUpdateView):
    template_name = 'admin/size/update.html'
    template_name_suffix = "_form"
    model = Size
    success_url = reverse_lazy('admin_size_index')
    fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AdminSizeUpdateView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "name", "slug", "description", "vcpu", "disk", "memory", "transfer", "price",
            InlineCheckboxes("regions", css_class="checkboxinput"),
            "is_active"
        )
            
    def get_form(self, form_class=None):
        form = super(AdminSizeUpdateView, self).get_form(form_class)
        form.fields["regions"] = CustomModelMultipleChoiceField(
            queryset=Region.objects.filter(is_deleted=False), 
            widget=forms.CheckboxSelectMultiple()
        )
        return form
    
    def get_context_data(self, **kwargs):
        context = super(AdminSizeUpdateView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context


class AdminSizeDeleteView(AdminDeleteView):
    template_name = 'admin/size/delete.html'
    model = Size
    success_url = reverse_lazy('admin_size_index')

    def delete(self, request, *args, **kwargs):
        size = self.get_object()
        size.delete()
        return super(self).delete(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(AdminSizeDeleteView, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
    
    def get_context_data(self, **kwargs):
        context = super(AdminSizeDeleteView, self).get_context_data(**kwargs)
        context['helper'] = self.helper
        return context
