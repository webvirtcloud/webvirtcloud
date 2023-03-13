from django.http import HttpResponse

from .utils import MetadataMixin


class MetadataV1Json(MetadataMixin):
    def get(self, request, *args, **kwargs):
        if self.virtance is None:
            return HttpResponse("Not Found", status=404)
        response = {
            "id": self.virtance.id,
            "hostname": self.virtance.name,
            "user-data": self.virtance.user_data,
            "vendor-data": "",
            "public-keys": "",
            "region": "",
            "interfaces": "",
            "dns": "",
        }
        return HttpResponse(response)


class MetadataIndex(MetadataMixin):
    def get(self, request, *args, **kwargs):
        if self.virtance is None:
            return HttpResponse("Not Found", status=404)
        data = ["id", "hostname", "user-data", "vendor-data", "public-keys", "region", "interfaces/", "dns/"]
        response = "\n".join(data)
        return HttpResponse(response)
