from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils import timezone


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT)
    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-id"]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(Project, self).save(*args, **kwargs)
