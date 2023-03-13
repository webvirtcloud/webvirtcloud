from django.urls import reverse_lazy
from virtance.models import Virtance
from admin.mixins import AdminTemplateView


class AdminVirtanceIndexView(AdminTemplateView):
    template_name = 'admin/virtance/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['virtances'] = Virtance.objects.filter(is_deleted=False)
        return context
