from partysense.event.models import Event, Location
from partysense.music.models import Track

from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    list_display = ("title", 'dj', "start_time", "location", 'number_of_tracks', 'number_of_users',
                    'past_event'
                    )
    fields = ("title", "description", 'location', 'user_editable', 'fb_url', 'djs', 'start_time')

admin.site.register(Event, EventAdmin)
admin.site.register(Location)
