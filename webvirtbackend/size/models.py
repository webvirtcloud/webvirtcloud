from django.db import models
from django.utils import timezone


class Size(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    vcpu = models.IntegerField()
    disk = models.BigIntegerField()
    memory = models.BigIntegerField()
    transfer = models.BigIntegerField()
    regions = models.ManyToManyField("region.Region", related_name="regions")
    is_active = models.BooleanField("Active", default=False)
    is_deleted = models.BooleanField("Deleted", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=6, default=0.0)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"
        ordering = ["memory", "vcpu", "disk", "transfer"]

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super(Size, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.deleted = timezone.now()
        self.is_deleted = True
        self.save()

    def __unicode__(self):
        return self.name
