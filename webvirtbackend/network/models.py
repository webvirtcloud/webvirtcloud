from django.db import models
from django.utils import timezone


class Network(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    COMPUTE = "compute"
    TYPE_CHOICES = (
        (PUBLIC, "Public"),
        (PRIVATE, "Private"),
        (COMPUTE, "Compute"),
    )
    IPv4 = 4
    IPv6 = 6
    VERSION_CHOICES = (
        (IPv4, "IPv4"),
        (IPv6, "IPv6"),
    )
    cidr = models.GenericIPAddressField()
    netmask = models.GenericIPAddressField()
    gateway = models.GenericIPAddressField()
    dns1 = models.GenericIPAddressField(default="0.0.0.0")
    dns2 = models.GenericIPAddressField(default="0.0.0.0")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=PUBLIC)
    version = models.IntegerField(choices=VERSION_CHOICES, default=IPv4)
    region = models.ForeignKey("region.Region", models.PROTECT)
    is_active = models.BooleanField("Active", default=True)
    is_deleted = models.BooleanField("Deleted", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Aggregate"
        verbose_name_plural = "Aggregates"
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Network, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted = timezone.now()
        self.is_deleted = True
        self.save()


class IPAddress(models.Model):
    network = models.ForeignKey(Network, models.PROTECT)
    virtance = models.ForeignKey("virtance.Virtance", models.PROTECT)
    address = models.GenericIPAddressField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "IP Address"
        verbose_name_plural = "IP Addresses"
        ordering = ["-id"]

    def __unicode__(self):
        return self.address

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(IPAddress, self).save(*args, **kwargs)
