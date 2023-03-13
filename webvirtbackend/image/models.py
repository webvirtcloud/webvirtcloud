from uuid import uuid4
from django.db import models
from django.utils import timezone


class Image(models.Model):

    CUSTOM = "custom"
    BACKUP = "backup"
    SNAPSHOT = "snapshot"
    APPLICATION = "application"
    DISTRIBUTION = "distribution"
    TYPE_CHOICES = [
        (CUSTOM, "Custom"),
        (BACKUP, "Backup"),
        (SNAPSHOT, "Snapshot"),
        (APPLICATION, "Application"),
        (DISTRIBUTION, "Distribution"),
    ]

    UNKNOWN = "unknown"
    DEBIAN = "debian"
    UBUNTU = "ubuntu"
    FEDORA = "fedora"
    CENTOS = "centos"
    ALMALINUX = "almalinux"
    ROCKYLINUX = "rockylinux"
    DISTRO_CHOICES = [
        (UNKNOWN, "Unknown"),
        (DEBIAN, "Debian"),
        (UBUNTU, "Ubuntu"),
        (FEDORA, "Fedora"),
        (CENTOS, "CentOS"),
        (ALMALINUX, "AlmaLinux"),
        (ROCKYLINUX, "Rocky Linux"),
    ]

    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=SNAPSHOT)
    md5sum = models.CharField(max_length=50)
    distribution = models.CharField(max_length=50, choices=DISTRO_CHOICES, default=UNKNOWN)
    description = models.TextField(blank=True, null=True)
    regions = models.ManyToManyField("region.Region", blank=True)
    file_name = models.CharField(max_length=100)
    file_size = models.BigIntegerField(blank=True, null=True)
    disk_size = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField("Active", default=False)
    is_deleted = models.BooleanField("Deleted", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Image, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted = timezone.now()
        self.save()
