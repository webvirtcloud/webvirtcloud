from uuid import UUID
from django.http.response import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer
from webvirtcloud.views import error_message_response


class ProjectDefaultAPI(APIView):
    class_serializer = ProjectSerializer

    def get_object(self, user):
        try:
            return Project.objects.get(user=user, is_default=True, is_deleted=False)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        projects = self.get_object(user=request.user)
        serilizator = self.class_serializer(projects, many=False)
        return Response({"project": serilizator.data})


class ProjectListAPI(APIView):
    class_serializer = ProjectSerializer

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(user=request.user, is_deleted=False)
        serilizator = self.class_serializer(projects, many=True)
        return Response({"projects": serilizator.data})

    def post(self, request, *args, **kwargs):
        serilizator = self.class_serializer(data=request.data)
        if serilizator.is_valid(raise_exception=True):
            serilizator.save(user=request.user)
        return Response(serilizator.data, status=status.HTTP_201_CREATED)


class ProjectDataAPI(APIView):
    class_serializer = ProjectSerializer

    def get_object(self, uuid, user):
        try:
            UUID(uuid, version=4)
        except ValueError:
            raise Http404
        try:
            return Project.objects.get(uuid=uuid, user=user)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, uuid, *args, **kwargs):
        project = self.get_object(uuid, request.user)
        serilizator = self.class_serializer(project, many=False)
        return Response({"project": serilizator.data})

    def put(self, request, uuid, *args, **kwargs):
        project = self.get_object(uuid, request.user)
        serilizator = self.class_serializer(project, data=request.data)
        if serilizator.is_valid(raise_exception=True):
            serilizator.save()
        return Response(serilizator.data)

    def delete(self, request, uuid, *args, **kwargs):
        project = self.get_object(uuid, request.user)
        if project.is_default:
            return error_message_response("You can not delete default project.")
        project.is_deleted = True
        project.deleted = timezone.now()
        project.save()
        return Response({"message": "Project deleted."})
