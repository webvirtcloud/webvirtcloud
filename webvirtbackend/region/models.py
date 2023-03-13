from django.db import models
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField("Active", default=False)
    is_deleted = models.BooleanField("Deleted", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Region, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.is_deleted = True
        self.deleted = timezone.now()
        self.save()

    def __unicode__(self):
        return self.name
