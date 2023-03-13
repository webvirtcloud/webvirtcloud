from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils import timezone


class Virtance(models.Model):
    ACTIVE = "active"
    PENDING = "pending"
    INACTIVE = "inactive"
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (PENDING, "Pending"),
        (INACTIVE, "Inactive"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    size = models.ForeignKey("size.Size", models.PROTECT)
    image = models.ForeignKey("image.Image", models.PROTECT)
    region = models.ForeignKey("region.Region", models.PROTECT)
    compute = models.ForeignKey("compute.Compute", models.PROTECT, null=True, blank=True)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)
    disk = models.BigIntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=PENDING)
    user_data = models.TextField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = "Virtance"
        verbose_name_plural = "Virtances"

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Virtance, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted = timezone.now()
        self.save()

    def __unicode__(self):
        return self.name
