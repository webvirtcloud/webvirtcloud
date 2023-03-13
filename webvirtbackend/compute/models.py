from uuid import uuid4
from django.db import models
from django.utils import timezone


class Compute(models.Model):
    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    ARCH_CHOICES = [
        (X86_64, "X64"),
        (AARCH64, "ARM64")
    ]
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    arch = models.CharField(max_length=50, choices=ARCH_CHOICES, default=X86_64)
    description = models.TextField()
    hostname = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    region = models.ForeignKey("region.Region", models.PROTECT)
    is_active = models.BooleanField("Active", default=True)
    is_deleted = models.BooleanField("Deleted",default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Compute"
        verbose_name_plural = "Computes"
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Compute, self).save(*args, **kwargs)

    def deletea(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save()