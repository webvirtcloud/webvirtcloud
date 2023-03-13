from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Image
from .serializers import ImageSerializer


class ImageListAPI(APIView):
    class_serializer = ImageSerializer

    def get_queryset(self):
        queryset = Image.objects.filter(is_deleted=False)
        image_type = self.request.query_params.get('type', None)
        if image_type is not None:
            queryset = queryset.filter(type=image_type)
        return queryset

    def get(self, request, *args, **kwargs):
        serilizator = self.class_serializer(self.get_queryset(), many=True)
        return Response({"images": serilizator.data})
