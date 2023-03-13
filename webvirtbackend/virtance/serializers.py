from django.db.models import Q
from rest_framework import serializers

from size.models import Size
from image.models import Image
from region.models import Region
from network.models import IPAddress
from keypair.models import KeyPair, KeyPairVirtance
from size.serializers import SizeSerializer
from image.serializers import ImageSerializer
from region.serializers import RegionSerializer
from compute.helper import WebVirtCompute
from .models import Virtance
from .tasks import create_virtance, action_virtance


class VirtanceSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    image = ImageSerializer()
    region = RegionSerializer()
    vcpu = serializers.IntegerField(source="size.vcpu")
    memory = serializers.IntegerField(source="size.memory")
    locked = serializers.BooleanField(source="is_locked")
    created_at = serializers.DateTimeField(source="created")
    disk = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    networks = serializers.SerializerMethodField()
    backup_ids = serializers.SerializerMethodField()
    snapshot_ids = serializers.SerializerMethodField()

    class Meta:
        model = Virtance
        fields = (
            "id",
            "name",
            "vcpu",
            "memory",
            "disk",
            "locked",
            "status",
            "created_at",
            "features",
            "backup_ids",
            "snapshot_ids",
            "image",
            "size",
            "networks",
            "region",
        )

    def get_status(self, obj):
        if obj.compute is not None:
            wvcomp = WebVirtCompute(obj.compute.token, obj.compute.hostname)
            if wvcomp.status_virtance(obj.id) == "running":
                return obj.ACTIVE
            if wvcomp.status_virtance(obj.id) == "shutoff":
                return obj.INACTIVE
        return obj.PENDING

    def get_disk(self, obj):
        return obj.disk // (1024 ** 3)

    def get_features(self, obj):
        return []

    def get_backup_ids(self, obj):
        return []

    def get_snapshot_ids(self, obj):
        return []

    def get_networks(self, obj):
        v4 = []
        v6 = []
        for ip in IPAddress.objects.filter(virtance=obj):
            if ip.network.version == ip.network.IPv6:
                v6.append({
                    "address": ip.address,
                    "prefix": ip.network.netmask,
                    "gateway": ip.network.gateway,
                    "type": ip.network.type,
                })
            else:
                v4.append({
                    "address": ip.address,
                    "netmask": ip.network.netmask,
                    "gateway": ip.network.gateway,
                    "type": ip.network.type,
                })
        return {"v4": v4, "v6": v6}


class CreateVirtanceSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    name = serializers.CharField(max_length=100)
    size = serializers.SlugField()
    image = serializers.CharField()
    region = serializers.SlugField()
    ipv6 = serializers.BooleanField(required=False)
    backups = serializers.BooleanField(required=False)
    password = serializers.CharField(required=False, allow_blank=True)
    keypairs = serializers.ListField(required=False, allow_empty=True)
    user_data = serializers.CharField(required=False, allow_blank=True)

 
    def validate(self, attrs):
        image = attrs.get("image")
        size = attrs.get("size")
        region = attrs.get("region")
        keypairs = attrs.get("keypairs")
        
        # Check if keypairs are active
        for k_id in keypairs:
            try:
                KeyPair.objects.get(id=k_id, user=self.context.get("request").user)
            except KeyPair.DoesNotExist:
                raise serializers.ValidationError({"keypairs": ["Invalid keypair ID."]})
        
        # Check if region is active
        try:
            check_region = Region.objects.get(slug=region, is_deleted=False)
            if check_region.is_active is False:
                raise serializers.ValidationError({"region": ["Region is not active."]})
        except Region.DoesNotExist:
            raise serializers.ValidationError({"region": ["Region not found."]})

        # Check if size is active
        try:
            check_size = Size.objects.get(slug=size, is_deleted=False)
            if check_size.is_active is False:
                raise serializers.ValidationError({"size": ["Size is not active."]})
        except Size.DoesNotExist:
            raise serializers.ValidationError({"size": ["Size not found."]})

        # Check if image is active
        if image.isdigit():
            try:
                check_image = Image.objects.get(
                    Q(type=Image.SNAPSHOT) | Q(type=Image.BACKUP) | Q(type=Image.CUSTOM),
                    id=image, is_deleted=False
                )
            except Image.DoesNotExist:
                raise serializers.ValidationError({"image": ["Image not found."]})
        else:
            try:
                check_image = Image.objects.get(
                    Q(type=Image.DISTRIBUTION) | Q(type=Image.APPLICATION),
                    slug=image, is_deleted=False
                )
                if check_image.is_active is False:
                    raise serializers.ValidationError({"image": ["Image is not active."]})
            except Image.DoesNotExist:
                raise serializers.ValidationError({"image": ["Image not found."]})

        # Check if size is available in region
        if check_region not in check_size.regions.all():
            raise serializers.ValidationError({"size": ["Size is not available in the region."]})
        
        # Check if image is available in region
        if check_region not in check_image.regions.all():
            raise serializers.ValidationError({"image": ["Image is not available in the region."]})
        
        return attrs
    
    def create(self, validated_data):
        ipv6 = validated_data.get("ipv6")
        name = validated_data.get("name")
        size = validated_data.get("size")
        region = validated_data.get("region")
        backups = validated_data.get("backups")
        password = validated_data.get("password")
        keypairs = validated_data.get("keypairs")
        user_data = validated_data.get("user_data")

        if validated_data.get("size").isdigit():
            image = Image.objects.get(id=validated_data.get("image"))
        else:
            image = Image.objects.get(slug=validated_data.get("image"))

        size = Size.objects.get(slug=validated_data.get("size"))
        region = Region.objects.get(slug=validated_data.get("region"))

        virtance = Virtance.objects.create(
            user=self.context.get("request").user,
            name=name,
            size=size,
            disk=size.disk,
            image=image,
            region=region,
            user_data=user_data
        )

        if keypairs:
            for k_id in keypairs:
                KeyPairVirtance.objects.create(keypair_id=k_id, virtance=virtance)

        if ipv6:
            pass

        if backups:
           pass

        create_virtance.delay(virtance.id, password=password)

        validated_data["id"] = virtance.id
        return validated_data


class VirtanceActionSerializer(serializers.Serializer):
    size = serializers.SlugField(required=False)
    name = serializers.CharField(max_length=100, required=False)
    image = serializers.CharField(required=False)
    action = serializers.CharField(max_length=20)
    password = serializers.CharField(required=False)

    def validate_action(self, value):
        actions = ["power_on", "power_off", "shutdown", "reboot", "password_reset", "resize", "rename", "rebuild"]
        if value not in actions:
            raise serializers.ValidationError({"action": ["Invalid action."]})
        return value

    def validate(self, attrs):
        if attrs.get("action") == "resize":
            if attrs.get("size") is None:
                raise serializers.ValidationError({"size": ["This field is required."]})
        if attrs.get("action") == "rename":
            if attrs.get("name") is None:
                raise serializers.ValidationError({"name": ["This field is required."]})
        if attrs.get("action") == "rebuild":
            if attrs.get("image") is None:
                raise serializers.ValidationError({"image": ["This field is required."]})
        if attrs.get("action") == "password_reset":
            if attrs.get("password") is None:
                raise serializers.ValidationError({"password": ["This field is required."]})
        return attrs
    
    def create(self, validated_data):
        action = validated_data.get("action")
        virtnace = validated_data.get("virtance")
        if action in ["power_on", "power_off", "shutdown", "reboot"]:
            action_virtance.delay(virtnace.id, action)
        return validated_data
