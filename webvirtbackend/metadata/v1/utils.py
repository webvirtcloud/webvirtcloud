from django.views.generic import View

from virtance.models import Virtance
from network.models import IPAddress


class MetadataMixin(View):
    virtance = None

    def dispatch(self, request, *args, **kwargs):
        x_instance_id = request.META.get("HTTP_X_INSTANCE_ID")
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        # Get by header ID
        if x_instance_id:
            try:
                self.virtance = Virtance.objects.get(pk=x_instance_id, is_deleted=False)
            except Virtance.DoesNotExist:
                pass

        # Get by IP address
        if not x_instance_id:
            if x_forwarded_for:
                remote_address = x_forwarded_for.split(",")[0]
            else:
                remote_address = request.META.get("REMOTE_ADDR")

            try:
                ip = IPAddress.objects.get(address=remote_address, virtance__is_deleted=False)
                if ip.virtance:
                    self.virtance = ip.virtance
            except IPAddress.DoesNotExist:
                pass

        return super(MetadataMixin, self).dispatch(request, *args, **kwargs)
