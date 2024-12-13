from django.contrib import admin

from .models import Website, SkillSet


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "created_at", "updated_at")
    search_fields = ("name", "url")
    list_filter = ("created_at", "updated_at")


class SkillSetAdmin(admin.ModelAdmin):
    list_display = ("skill_name", "country_name", "created_at", "updated_at")
    search_fields = ("skill_name", "country_name")
    list_filter = ("created_at", "updated_at")


admin.site.register(Website, WebsiteAdmin)
admin.site.register(SkillSet, SkillSetAdmin)
