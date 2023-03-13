from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Size
from .serializers import SizeSerializer


class SizeListAPI(APIView):
    class_serializer = SizeSerializer

    def get_queryset(self):
        return Size.objects.filter(is_deleted=False)

    def get(self, request, *args, **kwargs):
        serilizator = self.class_serializer(self.get_queryset(), many=True)
        return Response({"sizes": serilizator.data})
