from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from common.models import User

# Text to put at the end of each page's <title>.
admin.site.site_title = _("%(site)s Backoffice" % {"site": settings.SITE_NAME})

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = _("%(site)s administration" % {"site": settings.SITE_NAME})


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ("__str__", "is_staff", "date_joined")
    list_filter = ("is_staff", "is_active")
