from partysense.dj.models import DJ

from django.contrib import admin


class DJAdmin(admin.ModelAdmin):
    list_display = ("nickname", "user", "email", "url", "city_name")


admin.site.register(DJ, DJAdmin)

