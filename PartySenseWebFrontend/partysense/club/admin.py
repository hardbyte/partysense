from partysense.club.models import Club
from django.contrib import admin

class ClubAdmin(admin.ModelAdmin):
    list_display = ("club_id","club_name", "admin_user", "club_email", "club_website", "city", "country")


admin.site.register(Club, ClubAdmin)
