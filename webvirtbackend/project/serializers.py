from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    default = serializers.BooleanField(source="is_default", required=False)
    description = serializers.CharField(required=False)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ("uuid", "name", "default", "description", "created", "updated")

    def validate(self, attrs):
        name = attrs.get("name")
        description = attrs.get("description")

        if name and len(name) > 100:
            raise serializers.ValidationError("Name must be less than 100 characters long.")

        if description and len(description) > 255:
            raise serializers.ValidationError("Description must be less than 1000 characters long.")

        return attrs

    def create(self, validated_data):
        user = validated_data.get("user")
        name = validated_data.get("name")
        default = validated_data.get("is_default")
        description = validated_data.get("description")

        if default is True:
            Project.objects.filter(user=user).update(is_default=False)

        project = Project.objects.create(
            user=user,
            name=name,
            is_default=default,
            description=description,
        )

        return project

    def update(self, instance, validated_data):
        name = validated_data.get("name", instance.name)
        default = validated_data.get("is_default", instance.is_default)
        description = validated_data.get("description", instance.description)

        if default is True:
            Project.objects.filter(user=instance.user).update(is_default=False)

        instance.name = name
        instance.is_default = default
        instance.description = description
        instance.save()

        return instance
