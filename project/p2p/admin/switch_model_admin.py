from p2p.models import SwitchModel

from django.contrib import (
    admin,
)


@admin.register(SwitchModel)
class SwitchModelAdmin(admin.ModelAdmin):
    pass
