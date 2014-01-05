from partysense.dj.models import DJ

from django.contrib import admin


class DJAdmin(admin.ModelAdmin):
    list_display = ("nickname", "email", "url", "city_name")
    list_filter = ['city_name']
    search_fields = ['nickname', 'email']

admin.site.register(DJ, DJAdmin)

