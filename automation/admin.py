from django.contrib import admin

from .models import Website


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "created_at", "updated_at")
    search_fields = ("name", "url")
    list_filter = ("created_at", "updated_at")


admin.site.register(Website, WebsiteAdmin)
