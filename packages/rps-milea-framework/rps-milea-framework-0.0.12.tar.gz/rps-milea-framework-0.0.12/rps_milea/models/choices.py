from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from rps_milea.models.defaults import MileaModel


class MileaChoicesField(models.ForeignKey):
    """
    Define own Class so you can modify the queryset in admin.py
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ModelSelectField(models.ForeignKey):

    def __init__(self, *args, **kwargs):

        self.allowed_apps = settings.CUSTOM_APPS

        kwargs['to'] = ContentType
        kwargs['on_delete'] = models.CASCADE

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        qs = ContentType.objects.filter(app_label__in=self.allowed_apps)
        defaults = {'queryset': qs}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class MileaChoices(MileaModel):

    COLOR_CHOICES = [
        ('blue', 'Blue'),
        ('azure', 'Azure'),
        ('indigo', 'Indigo'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('red', 'Red'),
        ('orange', 'Orange'),
        ('yellow', 'Yellow'),
        ('lime', 'Lime'),
        ('green', 'Green'),
        ('teal', 'Teal'),
        ('cyan', 'Cyan'),
        ('dark', 'Black'),
        ('muted', 'Gray')
    ]

    model = ModelSelectField()
    display = models.CharField(max_length=64, verbose_name=_("Display name"))
    color = models.CharField(max_length=16, choices=COLOR_CHOICES, verbose_name=_("Color"))
    value = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        self.value = slugify(self.display)
        super().save(*args, **kwargs)

    def __html__(self):
        return format_html('<span class="badge bg-{} text-{}-fg me-1">{}</span>', self.color, self.color, self.display)

    def __str__(self):
        return self.display

    class Meta:
        ordering = ['model', 'value']
        verbose_name = _("Selection box")
        verbose_name_plural = _("Selection boxes")
