from decimal import Decimal
from rest_framework import serializers

from .models import Image
from region.models import Region


class ImageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    public = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()
    distribution = serializers.SerializerMethodField()
    min_disk_size = serializers.SerializerMethodField()
    size_gigabytes = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source="created")

    class Meta:
        model = Image
        fields = (
            "slug",
            "name",
            "distribution",
            "regions",
            "public",
            "created_at",
            "type",
            "description",
            "min_disk_size",
            "size_gigabytes",
            "status",
        )

    def get_regions(self, obj):
        if obj.type == obj.DISTRIBUTION or obj.type == obj.APPLICATION:
            return [region.slug for region in obj.regions.all()]
        return []

    def get_public(self, obj):
        if obj.type == obj.DISTRIBUTION or obj.type == obj.APPLICATION:
            return True
        return False

    def get_status(self, obj):
        if obj.is_active is True:
            return "available"
        return "unavailable"

    def get_distribution(self, obj):
        for distro in obj.DISTRO_CHOICES:
            if distro[0] == obj.distribution:
                return distro[1]

    def get_min_disk_size(self, obj):
        if obj.type == obj.DISTRIBUTION or obj.type == obj.APPLICATION:
            return 0
        return obj.disk_size / 1073741824

    def get_size_gigabytes(self, obj):
        if obj.type == obj.DISTRIBUTION or obj.type == obj.APPLICATION:
            return 0
        return Decimal(obj.file_size) / Decimal(1073741824)
