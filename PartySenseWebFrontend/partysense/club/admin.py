from partysense.club.models import Club
from django.contrib import admin


class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "website", "city", "country")


admin.site.register(Club, ClubAdmin)
