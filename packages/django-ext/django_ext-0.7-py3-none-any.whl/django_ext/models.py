from django.db import models
from django.utils.translation import gettext_lazy as _
from django_currentuser.db.models import CurrentUserField


class TimestampModel(models.Model):
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        abstract = True


class TimeRangeModel(models.Model):
    started_at = models.DateTimeField(_('started at'), null=True, blank=True)
    ended_at = models.DateTimeField(_('ended at'), null=True, blank=True)

    class Meta:
        abstract = True


class UserTrackModel(models.Model):
    created_by = CurrentUserField(on_delete=models.PROTECT, related_name='+', verbose_name=_('created by'))
    updated_by = CurrentUserField(on_delete=models.PROTECT, on_update=True, related_name='+', verbose_name=_('updated by'))

    class Meta:
        abstract = True
