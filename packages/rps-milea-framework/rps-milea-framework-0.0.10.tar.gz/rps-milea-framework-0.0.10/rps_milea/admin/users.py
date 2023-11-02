from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from email_users.admin import UserAdmin
from email_users.models import User

# Milea User Admin
admin.site.unregister(User)
@admin.register(User)
class NewUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'is_active')
    list_filter = ("is_active",)  # Attention, do not allow groups, because other users will see all existing groups. Issue #10
    search_fields = ('email',)
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('id',)

    fieldsets = (
        (_("Personal info"), {'fields': (('email', 'password'), ('first_name', 'last_name'),)}),
        (_("Permissions"), {"fields": ('is_active', 'is_staff', 'groups',)}),
        (_("Important dates"), {'fields': (('last_login', 'date_joined'),)}),
    )

    add_fieldsets = (
        (_("Personal info"), {'fields': ('email', ('password1', 'password2'), ('first_name', 'last_name'),)}),
        (_("Permissions"), {"fields": ('is_active', 'is_staff', 'groups',)}),
    )

    admin_fieldsets = (
        (_("Administration"), {"fields": ('is_superuser', 'user_permissions')}),
    )

    def get_fieldsets(self, request, obj=None):
        # Hole die standardmäßigen Felder, die von Django automatisch generiert werden
        fieldsets = super().get_fieldsets(request, obj=obj)

        # Füge Adminfieldset hinzu
        if request.user.is_superuser:
            fieldsets += self.admin_fieldsets

        return fieldsets

    # Modify Form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['is_staff'].initial = True
        form.base_fields['groups'].required = True
        return form

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'groups' and not request.user.is_superuser:
            kwargs["queryset"] = request.user.groups.all()
            return db_field.formfield(**kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Modify QS for non superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Only show Objects for user group
        if not request.user.is_superuser:
            qs = qs.filter(groups__in=request.user.groups.all())
            qs = qs.filter(is_superuser=False)
            qs = qs.distinct()  # Remove multiple users if user has more than one group

        return qs
