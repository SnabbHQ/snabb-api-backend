"""AppInfo models."""

from datetime import datetime
from django.db import models
from django.utils.dateformat import format


class AppInfo(models.Model):
    """AppInfo Model."""

    appInfo_id = models.AutoField(
        primary_key=True, blank=True, editable=False
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(max_length=300, null=True, blank=True)
    updatedAt = models.IntegerField(default=0, editable=False)
    active = models.BooleanField(default=True)
    updated_at = models.IntegerField(default=0, editable=False)
    created_at = models.IntegerField(default=0, editable=False, blank=True)

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'AppInfo',
        verbose_name_plural = u'AppsInfo'

    def save(self, *args, **kwargs):
        self.updated_at = int(format(datetime.now(), u'U'))

        if not self.appInfo_id:
            self.created_at = int(format(datetime.now(), u'U'))
        else:
            self.updated_at = int(format(datetime.now(), u'U'))

        super(AppInfo, self).save(*args, **kwargs)
