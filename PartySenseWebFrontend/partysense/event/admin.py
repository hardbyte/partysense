from partysense.event.models import Event, Location
from partysense.music.models import Track

from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "dj", "start_time", "location",
                    #"tracks",
                    )

admin.site.register(Event, EventAdmin)
admin.site.register(Location)
