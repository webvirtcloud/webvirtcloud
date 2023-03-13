from base64 import b64decode, binascii
from rest_framework import serializers

from .models import KeyPair


class KeyPairSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=False)
    public_key = serializers.CharField(max_length=1000, required=False)
    fingerprint = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, source="created")

    class Meta:
        model = KeyPair
        fields = (
            "id",
            "name",
            "public_key",
            "fingerprint",
            "created_at",
        )

    def validate_public_key(self, value):
        if not value.startswith("ssh-rsa"):
            raise serializers.ValidationError("Invalid public key format.")
        if len(value.strip().split()) <= 1:
            raise serializers.ValidationError("Invalid public key format.")
        try:
            b64decode(value.strip().split()[1])
        except (TypeError, binascii.Error):
            raise serializers.ValidationError("Invalid public key format.")
        
        try:
            KeyPair.objects.get(public_key=value)
            raise serializers.ValidationError("Key already exists.")
        except KeyPair.DoesNotExist:
            pass

        return value

    def update(self, instance, validated_data):
        if not validated_data.get("name"):
            raise serializers.ValidationError(
                {"name": ["This field is required."]}
            )

        if validated_data.get("name"):
            instance.name = validated_data.get("name", instance.name)
        
        instance.save()
        return instance

    def create(self, validated_data):
        errors = {}
        if not validated_data.get("name"):
            errors["name"] = ["This field is required."]
        if not validated_data.get("public_key"):
            errors["public_key"] = ["This field is required."]
        if errors:
            raise serializers.ValidationError(errors)
        return KeyPair.objects.create(**validated_data)
