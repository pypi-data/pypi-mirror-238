from django import forms
from django.contrib import admin
from django.forms.widgets import Select
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from rps_milea.admin.defaults import MileaAdmin
from rps_milea.models.choices import MileaChoices


class TablerColorPickerWidget(Select):
    template_name = 'django/forms/widgets/colorpicker.html'


class MileaChoicesForm(forms.ModelForm):
    class Meta:
        model = MileaChoices
        fields = ('display', 'model', 'color')

    color = forms.ChoiceField(
        widget=TablerColorPickerWidget(),
        choices=MileaChoices.COLOR_CHOICES
    )


@admin.register(MileaChoices)
class MileaChoicesAdmin(MileaAdmin):
    form = MileaChoicesForm
    list_display = ('display', 'model', 'badge')
    list_display_links = ('display',)
    show_sysdata = True

    fieldsets = (
        (None, {
            'fields': (
                ('model', 'display'), 'color',
            ),
        }),
    )

    def badge(self, obj):
        return format_html(
            '<span class="badge bg-{} text-{}-fg">{}</span>', obj.color, obj.color, obj.get_color_display(),
        )
    badge.short_description = _("Color")

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['model',]
        return self.readonly_fields
