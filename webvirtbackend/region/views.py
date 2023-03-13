from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Region
from .serializers import RegionSerializer


class RegionListAPI(APIView):
    class_serializer = RegionSerializer

    def get_queryset(self):
        return Region.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        serilizator = self.class_serializer(self.get_queryset(), many=True)
        return Response({"regions": serilizator.data})
