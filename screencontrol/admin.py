from django.contrib import admin, messages

# Register your models here.
from django.utils.translation import ngettext

from screencontrol.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'name', 'allowed_control',)
    actions = ['allow_control_to_clients', ]

    def allow_control_to_clients(self, request, queryset):
        updated = queryset.update(allowed_control=True)
        self.message_user(request, ngettext(
            '%d client was successfully allowed control.',
            '%d clients were successfully allowed control.',
            updated,
        ) % updated, messages.SUCCESS)

    allow_control_to_clients.short_description = 'Grant control to selected clients'


admin.site.register(Client, ClientAdmin)
