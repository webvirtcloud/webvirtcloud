from decimal import Decimal
from rest_framework import serializers

from .models import Size
from region.models import Region


class SizeSerializer(serializers.ModelSerializer):
    available = serializers.BooleanField(source="is_active")
    price_hourly = serializers.DecimalField(source="price", max_digits=10, decimal_places=6)
    price_monthly = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    memory = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()
    transfer = serializers.SerializerMethodField()

    class Meta:
        model = Size
        fields = (
            "slug",
            "memory",
            "vcpu",
            "disk",
            "transfer",
            "description",
            "available",
            "price_hourly",
            "price_monthly",
            "regions",
        )

    def get_disk(self, obj):
        return obj.disk // 1073741824

    def get_memory(self, obj):
        return obj.memory // 1048576

    def get_transfer(self, obj):
        return obj.transfer / 1099511627776

    def get_price_monthly(self, obj):
        return int(round(obj.price * 730, 0))

    def get_regions(self, obj):
        return [region.slug for region in obj.regions.all()]
