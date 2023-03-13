import base64
import hashlib
from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils import timezone


class KeyPair(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    public_key = models.CharField(max_length=1000)
    fingerprint = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SSH Key"
        verbose_name_plural = "SSH Keys"
        ordering = ["-id"]

    def make_fingerprint(self):
        p_bytes = base64.b64decode(self.public_key.strip().split()[1])
        fp_plain = hashlib.md5(p_bytes).hexdigest()
        self.fingerprint = ":".join([fp_plain[i : i + 2] for i in range(0, len(fp_plain), 2)])

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        self.make_fingerprint()
        super(KeyPair, self).save(*args, **kwargs)


class KeyPairVirtance(models.Model):
    keypair = models.ForeignKey(KeyPair, models.CASCADE)
    virtance = models.ForeignKey("virtance.Virtance", models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SSH Key Virtance"
        verbose_name_plural = "SSH Keys Virtance"
        ordering = ["-id"]
