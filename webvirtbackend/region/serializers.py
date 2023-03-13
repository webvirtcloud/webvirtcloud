from rest_framework import serializers

from .models import Region
from size.models import Size


class RegionSerializer(serializers.ModelSerializer):
    available = serializers.BooleanField(source="is_active")
    features = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ("slug", "name", "available", "features", "sizes")

    def get_features(self, obj):
        return []

    def get_sizes(self, obj):
        return [size.slug for size in Size.objects.filter(is_deleted=False) if obj in size.regions.all()]
