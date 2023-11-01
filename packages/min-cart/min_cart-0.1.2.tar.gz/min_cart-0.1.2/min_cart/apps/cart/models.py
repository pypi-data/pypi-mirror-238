
from django.utils.translation import gettext_lazy as _
from django.db import models


class AbstractAddress(models.Model):
    first_name = models.CharField(_("First name"), max_length=255, blank=True)


    class Meta:
        abstract = True
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')